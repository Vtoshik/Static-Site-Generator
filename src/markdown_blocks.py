from enum import Enum
import re

class BlockType(Enum): 
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.splitlines()
    if not lines:
        return BlockType.PARAGRAPH

    if re.match(r'^(#{1,6})\s', lines[0]):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE 
    elif all(re.match(r'^-\s', line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    ordered_list_pattern = r'^(\d+)\.\s'
    expected_number = 1

    for line in lines:
        match = re.match(ordered_list_pattern, line)
        if not match:
            break
        num = int(match.group(1))
        if num != expected_number:
            break
        expected_number += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    splited = markdown.split('\n\n')
    blocks = [block.strip() for block in splited]
    striped = [block for block in blocks if block != ""]

    return striped