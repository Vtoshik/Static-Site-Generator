import os 
import logging
from markdown_blocks import markdown_to_html_node

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        lines = block.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("# ") and not line.startswith("##"):
                return line[2:].strip()
    raise ValueError("No h1 header found in Markdown")

def generate_page(from_path,template_path,dest_path):
    """
    Generate an HTML page from a Markdown file using a template.

    Args:
        from_path (str): Path to the input Markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path where the output HTML file will be written.

    Raises:
        FileNotFoundError: If the Markdown or template file does not exist.
        ValueError: If the Markdown file has no h1 header or other parsing errors.
    """
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the Markdown file
    if not os.path.exists(from_path):
        logging.error(f"Markdown file {from_path} does not exist")
        raise FileNotFoundError(f"Markdown file {from_path} does not exist")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Read the template file
    if not os.path.exists(template_path):
        logging.error(f"Template file {template_path} does not exist")
        raise FileNotFoundError(f"Template file {template_path} does not exist")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Convert Markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)

    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Write the final HTML to the destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    logging.info(f"Generated HTML file at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively crawl the content directory and generate HTML pages for each Markdown file.

    Args:
        dir_path_content (str): Path to the content directory containing Markdown files.
        template_path (str): Path to the HTML template file.
        dest_dir_path (str): Path to the destination directory for generated HTML files.

    Raises:
        FileNotFoundError: If the content directory or template file does not exist.
        ValueError: If a Markdown file has no h1 header or other parsing errors.
    """
    # Check if content directory exists
    if not os.path.exists(dir_path_content):
        logging.error(f"Content directory {dir_path_content} does not exist")
        raise FileNotFoundError(f"Content directory {dir_path_content} does not exist")

    # Check if template file exists
    if not os.path.exists(template_path):
        logging.error(f"Template file {template_path} does not exist")
        raise FileNotFoundError(f"Template file {template_path} does not exist")

    # Crawl the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Construct full paths
                markdown_path = os.path.join(root, file)
                
                # Calculate relative path and corresponding destination path
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_filename = os.path.splitext(relative_path)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, html_filename)

                # Generate the HTML page
                try:
                    generate_page(markdown_path, template_path, dest_path)
                except Exception as e:
                    logging.error(f"Failed to generate page for {markdown_path}: {str(e)}")
                    raise
