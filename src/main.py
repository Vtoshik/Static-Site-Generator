import os
import shutil
import logging
from markdown_utils import generate_pages_recursive

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def copy_directory(src, dst):
    """
    Recursively copy all contents from src directory to dst directory.
    Deletes all contents of dst directory before copying.

    Args:
        src (str): Path to source directory
        dst (str): Path to destination directory
    """
    # Check if source directory exists
    if not os.path.exists(src):
        logging.error(f"Source directory {src} does not exist")
        raise FileNotFoundError(f"Source directory {src} does not exist")
    
    # Remove destination directory if it exists
    if os.path.exists(dst):
        try:
            logging.info(f"Removing existing desination directory: {dst}")
            shutil.rmtree(dst)
        except Exception as e:
            logging.error(f"Failed to remove {dst}: {str(e)}")
            raise

    # Create destination directory
    os.mkdir(dst)
    logging.info(f"Created destination directory: {dst}")

    # Get all items in source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            # Copy file and log the action
            shutil.copy(src_path, dst_path)
            logging.info(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            # Recursively copy directory
            logging.info(f"Copying directory: {src_path}")
            copy_directory(src_path, dst_path)

def main():
    """
    Main function to generate the static site.
    - Deletes the public directory if it exists.
    - Copies static files from static to public.
    - Generates HTML pages for all Markdown files in content/ using template.html.
    """
    public_dir = "public"
    static_dir = "static"
    content_dir = "content"
    template_path = "template.html"

    try:
        # Delete the public directory if it exists
        if os.path.exists(public_dir):
            logging.info(f"Removing existing public directory: {public_dir}")
            shutil.rmtree(public_dir)

        # Copy static files to public
        copy_directory(static_dir, public_dir)

        # Generate HTML pages for all Markdown files
        generate_pages_recursive(content_dir, template_path, public_dir)

    except Exception as e:
        logging.error(f"Error during site generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()