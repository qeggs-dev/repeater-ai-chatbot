from ....._resource import Resource
from ......Context_Manager import (
    ContentRole
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .._responses import RoleStructureCheckerResponse

@Resource.app.get("/userdata/context/structure_check/role/{user_id}")
async def check_role_structure(user_id: str):
    """
    Endpoint to check the role structure error of a user's context.

    Args:
        user_id (str): The user ID
    
    Returns:
        ORJSONResponse: The response containing the context role structure error.
    """
    # 从chat.context_manager中加载用户ID为user_id的上下文
    context_loader = await Resource.core.get_context_loader()
    context = await context_loader.load_context(user_id)
    
    logger.info(
        "Checking role structure error",
        user_id = user_id,
    )

    role_rule = [
        [
            ContentRole.USER,
            ContentRole.FUNCTION
        ],
        [
            ContentRole.ASSISTANT
        ]
    ]

    for index, content in enumerate(context.context_list):
        expected_role = role_rule[index % len(role_rule)]
        if content.role not in expected_role:
            display_expected_role = [role.value for role in expected_role]
            return ORJSONResponse(
                content = RoleStructureCheckerResponse(
                    message = f"At index {index}, expected role is ({' or '.join(display_expected_role)}), but got {content.role.value}",
                    index = index,
                    role = content.role.value,
                    expected_role = display_expected_role,
                ).model_dump(exclude_none=True),
                status_code = 500
            )
    
    return ORJSONResponse(
        content = RoleStructureCheckerResponse().model_dump(exclude_none=True),
        status_code = 200
    )