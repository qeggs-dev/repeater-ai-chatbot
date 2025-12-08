from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from typing import Iterable
import re

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeBlockPreprocessor(md), 'code_block', 30)

class CodeBlockPreprocessor(Preprocessor):
    FIND_BIG_CODE_BLOCK_PATTERN = re.compile(r'```.*?```', re.DOTALL)
    FIND_LITTLE_CODE_BLOCK_PATTERN = re.compile(r'`.*?`', re.DOTALL)
    def run(self, lines:Iterable[str]):
        # 合并所有行
        text = "\n".join(lines)

        # 查找大代码块
        big_code_blocks = self.FIND_BIG_CODE_BLOCK_PATTERN.findall(text)
        for big_code_block in big_code_blocks:
            text = text.replace(big_code_block, f'<pre><code>{big_code_block}</code></pre>')

        # 查找小代码块
        little_code_blocks = self.FIND_LITTLE_CODE_BLOCK_PATTERN.findall(text)
        for little_code_block in little_code_blocks:
            text = text.replace(little_code_block, f'<code>{little_code_block}</code>')

        # 将文本分割回行
        return text.split('\n')
    

def makeExtension(**kwargs):
    return CodeBlockPreprocessor(**kwargs)