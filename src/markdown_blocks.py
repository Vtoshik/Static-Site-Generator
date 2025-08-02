def markdown_to_blocks(markdown):
    splited = markdown.split('\n\n')
    blocks = [block.strip() for block in splited]
    striped = [block for block in blocks if block != ""]

    return striped