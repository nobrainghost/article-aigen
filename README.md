# AI Content Generator

A Python tool that generates SEO-optimized articles with AI based on user topics, preferred length, and backlinks.

## Features

- Generate SEO-optimized articles on any topic
- Customize article length (small-800, medium-1200-1600, or long-1800+)
- Automatically insert backlinks at appropriate points in the content
- Include SEO-optimized images with alt text
- Export to MDX format with proper frontmatter
- Easily Swap Out Models - Currently Gemini Models
- Post Process (With AI image generation/ Simple - No AI/Simple With AI - No image generation)

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

### Single Article Mode

```bash
python src/article_generator.py \
  --topic "Sustainable Gardening Practices" \
  --length long \
  --backlinks '[{"https://example.com/gardening-tools":"gardening tools to make the job easier"},{"https://example.com/composting":"how to start composting at home"}]' \
  --output-dir "./blog-posts" \
  --model "gemini-1.5-pro"
```

### Bulk Processing Mode

Process multiple articles from a JSON file:

```bash
python src/article_generator.py \
  --bulk-file "articles.json" \
  --output-dir "./blog-posts" \
  --model "gemini-1.5-flash"
```

Or using the shell script:

```bash
./generate_article.sh --file "articles.json" --output "./blog-posts"
```

### Command Line Arguments

- `--topic`: The main topic for your article (required for single article mode)
- `--bulk-file`: JSON file containing multiple article configs for bulk processing
- `--length`: Article length preset (small: ~800 words, medium: ~1500 words, long: ~2200 words)
- `--backlinks`: JSON string containing backlinks and their descriptions
- `--output-dir`: Directory where the generated MDX file will be saved
- `--model`: Google AI model to use (gemini-1.5-pro, gemini-1.5-flash, gemini-pro)
- `--api-key`: Google AI API key (can also be set via GOOGLE_API_KEY environment variable)

### Image Post-Processing

After generating articles, you can enhance them with AI-generated images using the post-processor:

```bash
# Set your Together API key first
export TOGETHER_API_KEY="your-together-api-key-here"

# For using Gemini for image descriptions, also set this:
export GEMINI_API_KEY="your-gemini-api-key-here"

# Run the post-processor script and select an article interactively
./post_process_article.sh

# Or specify an article directly
./post_process_article.sh --article "articles/my-article.mdx" --images 4

# Use Gemini for image descriptions instead of Together AI
./post_process_article.sh --article "articles/my-article.mdx" --model gemini
```

The post-processor will:
1. Generate detailed image descriptions based on the article content (using either Together AI or Gemini)
2. Create AI-generated images for those descriptions (using Together AI)
3. Insert the images at appropriate locations in the article
4. Save the enhanced article to the `postprocessed` directory

#### Command Line Arguments for Post-Processor

- `--article`: Path to a specific article to process
- `--images`: Number of images to generate and insert (default: 3)
- `--output-dir`: Directory to save processed articles (default: ./postprocessed)
- `--model`: Model source for image descriptions (`together` or `gemini`)
- `--api-key`: Together AI API key (can also be set via TOGETHER_API_KEY environment variable)
- `--gemini-api-key`: Gemini API key (can also be set via GEMINI_API_KEY environment variable)

## Customization

You can modify the `ArticleGenerator` class to:

- Change the word count presets
- Add more AI models
- Customize the frontmatter format
- Change image placement rules

### Mini Post-Processor for Pexels Images

For a lighter, faster approach to enhancing articles with images, you can use the mini post-processor that uses Pexels API:

```bash
# Set your Pexels API key first
export PEXELS_API_KEY="your-pexels-api-key-here"

# Run in interactive mode to select an article
./mini_process_article.sh

# Process a specific article
./mini_process_article.sh --article "blog-posts/my-article.mdx"

# Process all articles automatically
./mini_process_article.sh --auto
```

The mini post-processor will:
1. Extract relevant keywords from the article
2. Search Pexels API for images matching those keywords
3. Hotlink directly to Pexels images using Next.js Image component for optimization
4. Insert one image after the title and three more throughout the article
5. Include proper attribution for Pexels photographers with clickable images
6. Save the enhanced article to the `miniprocessed` directory

#### Command Line Arguments for Mini Post-Processor

- `--article`: Path to a specific article to process
- `--output-dir`: Directory to save processed articles (default: ./miniprocessed)
- `--auto`: Process all articles automatically (non-interactive mode)
- `--api-key`: Pexels API key (can also be set via PEXELS_API_KEY environment variable)
- `--verbose`: Enable verbose logging

## Future Plans

- [x] Add option to use Gemini instead of Together AI for generating image descriptions
- [x] Add lightweight post-processor using Pexels API for direct image sourcing
- [ ] Add a research mode for factual context
- [ ] Add tone selection (professional, casual, educational, etc.)
- [ ] Vary article types by intent (how-to, listicle, news, etc.)
- [ ] Add SEO scoring algorithm
- [ ] Add competitor analysis
- [ ] Switch to Langraph and Process it as a State

## License

MIT
