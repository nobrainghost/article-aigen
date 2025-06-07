#!/bin/bash
# Generate SEO Article Script
# A helper script to simplify running the article generator

# Default values
TOPIC=""
LENGTH="medium"
BACKLINKS="[]"
OUTPUT_DIR="./articles"
MODEL="gemini-1.5-flash" #rate limiting/minute on 1.5 pro suucks

# Display help message
show_help() {
  echo "AI SEO Article Generator"
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -t, --topic TOPIC      Article topic (required)"
  echo "  -l, --length LENGTH    Article length: small, medium, or long (default: medium)"
  echo "  -b, --backlinks JSON   JSON string of backlinks (default: [])"
  echo "  -o, --output DIR       Output directory (default: ./articles)"
  echo "  -m, --model MODEL      Google AI model to use (default: gemini-1.5-pro)"
  echo "  -h, --help             Show this help message"
  echo ""
  echo "Example:"
  echo "$0 --topic \"Sustainable Gardening\" --length long"
  echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -t|--topic)
      TOPIC="$2"
      shift
      shift
      ;;
    -l|--length)
      LENGTH="$2"
      shift
      shift
      ;;
    -b|--backlinks)
      BACKLINKS="$2"
      shift
      shift
      ;;
    -o|--output)
      OUTPUT_DIR="$2"
      shift
      shift
      ;;
    -m|--model)
      MODEL="$2"
      shift
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $key"
      show_help
      exit 1
      ;;
  esac
done

# Check if TOPIC is provided
if [ -z "$TOPIC" ]; then
  echo "Error: Topic is required"
  show_help
  exit 1
fi

if [ -z "$GOOGLE_API_KEY" ]; then
  echo "Error: GOOGLE_API_KEY environment variable is not set"
  echo "Please set it with: export GOOGLE_API_KEY=your-api-key"
  exit 1
fi

# Run the article generator
echo "Generating $LENGTH article on: $TOPIC"
python src/article_generator.py \
  --topic "$TOPIC" \
  --length "$LENGTH" \
  --backlinks "$BACKLINKS" \
  --output-dir "$OUTPUT_DIR" \
  --model "$MODEL"

echo "Done!"
