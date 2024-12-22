import json
import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

logging.basicConfig(level=logging.INFO)


def sanitize_unicode(text):
    """Sanitize text to handle invalid Unicode characters."""
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")


def truncate_text(text, max_length=5000):
    """Truncate text to fit within the model's context window."""
    return text[:max_length]


def log_error(post, error):
    """Log errors with detailed information."""
    logging.error(f"Error processing post: {post}. Error: {error}")


def get_unified_tags(posts, processed_file_path):
    """Extract and save unique tags from all posts."""
    unified_tags = set()
    for post in posts:
        if "tags" in post:
            unified_tags.update(post["tags"])

    if processed_file_path != "None":
        tags_file_path = processed_file_path.replace("processed_posts.json", "tags.json")
        with open(tags_file_path, "w", encoding="utf-8") as tags_file:
            json.dump(list(unified_tags), tags_file, ensure_ascii=False, indent=4)

    return list(unified_tags)


def process_posts(raw_file_path, processed_file_path="None"):
    enriched_posts = []
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)
        for post in posts:
            try:
                # Sanitize text to avoid UnicodeEncodeError
                post['text'] = sanitize_unicode(post['text'])
                metadata = extract_metadata(post['text'])
                post_with_metadata = post | metadata
                enriched_posts.append(post_with_metadata)
            except Exception as e:
                log_error(post, e)

    # Save the processed posts to a file if a path is provided
    if processed_file_path != "None":
        with open(processed_file_path, "w", encoding="utf-8") as outfile:
            json.dump(enriched_posts, outfile, ensure_ascii=False, indent=4)

    # Get and save unique tags
    unified_tags = get_unified_tags(enriched_posts, processed_file_path)
    logging.info(f"Unified Tags: {unified_tags}")

    for epost in enriched_posts:
        print(epost)


def extract_metadata(post):
    template = '''
       You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
       1. Return a valid JSON. No preamble. 
       2. JSON object should have exactly three keys: line_count, language and tags. 
       3. tags is an array of text tags. Extract maximum two tags.
       4. Language should be English or Hinglish (Hinglish means Hindi + English)

       Here is the actual post on which you need to perform this task:  
       {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": truncate_text(post)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        res["tags"] = [tag for tag in res["tags"] if tag.lower() not in ["english", "hinglish"]]
    except OutputParserException:
        logging.error(f"Failed to parse response for post: {post}")
        res = {"line_count": 0, "language": "Unknown", "tags": []}
    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
