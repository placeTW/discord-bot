

def split_text(text: str, max_length: int = 2000) -> list[str]:
  chunks = []
  current_chunk = ""

  for line in text.splitlines(keepends=True):  # keepends=True keeps the newline characters
      if len(current_chunk) + len(line) <= max_length:
          current_chunk += line
      else:
          chunks.append(current_chunk)
          current_chunk = line

  if current_chunk:  # Append any remaining text
      chunks.append(current_chunk)

  return chunks