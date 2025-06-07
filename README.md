# AI Content Generator

A Python tool that generates SEO-optimized articles with AI based on user topics, preferred length, and backlinks.

## Features

- Generate SEO-optimized articles on any topic
- Customize article length (small-800, medium-1200-1600, or long-1800+)
- Automatically insert backlinks at appropriate points in the content
- Include SEO-optimized images with alt text
- Export to MDX format with proper frontmatter
- Easily Swap Out Models - Currently Gemini Models

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set your Google AI API key:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

### Basic Usage

```bash
python src/article_generator.py --topic "Your Article Topic" --length medium
```

### Advanced Options

```bash
python src/article_generator.py \
  --topic "Sustainable Gardening Practices" \
  --length long \
  --backlinks '[{"https://example.com/gardening-tools":"gardening tools to make the job easier"},{"https://example.com/composting":"how to start composting at home"}]' \
  --output-dir "./blog-posts" \
  --model "gemini-1.5-pro"
```

### Command Line Arguments

- `--topic` (required): The main topic for your article
- `--length`: Article length preset (small: ~800 words, medium: ~1500 words, long: ~2200 words)
- `--backlinks`: JSON string containing backlinks and their descriptions
- `--output-dir`: Directory where the generated MDX file will be saved
- `--model`: Google AI model to use (gemini-1.5-pro, gemini-1.5-flash, gemini-pro)
- `--api-key`: Google AI API key (can also be set via GOOGLE_API_KEY environment variable)

## Example Backlinks Format

```json
[
  {"https://example.com/page1": "description of first resource"},
  {"https://example.com/page2": "description of second resource"}
]
```

## Output

The script generates an MDX file with:

- SEO-optimized frontmatter (title, description, keywords)
- Well-structured markdown content with headings
- Naturally placed backlinks (at least 4 if provided)
- Image placeholders with descriptive alt text
- SEO-friendly filename based on the topic

## Customization

You can modify the `ArticleGenerator` class to:

- Change the word count presets
- Add more AI models
- Customize the frontmatter format
- Change image placement rules

## Future Plans

- [ ] Add a research mode for factual context
- [ ] Add tone selection (professional, casual, educational, etc.)
- [ ] Vary article types by intent (how-to, listicle, news, etc.)
- [ ] Add SEO scoring algorithm
- [ ] Add competitor analysis
- [ ] Switch to Langraph and Process it as a State

## License

MIT
