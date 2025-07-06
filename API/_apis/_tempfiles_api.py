from .._resource import app, chat, configs, validate_path
from fastapi import HTTPException
from fastapi.responses import FileResponse

@app.get("/file/render/{file_uuid}.png", name = "render_file")
async def get_render_file(file_uuid: str):
    """
    Endpoint for rendering file
    """
    rendered_image_dir = configs.get_config("rendered_image_dir", "./temp/render").get_value(Path)
    # 防止遍历攻击
    if not validate_path(rendered_image_dir, file_uuid):
        raise HTTPException(status_code=400, detail="Invalid file UUID")
    
    # 检查文件是否存在
    if not (rendered_image_dir / f"{file_uuid}.png").exists():
        raise HTTPException(detail="File not found", status_code=404)
    
    # 返回文件
    return FileResponse(rendered_image_dir / f"{file_uuid}.png")