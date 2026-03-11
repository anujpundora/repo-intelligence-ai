import os

CHUNK_SIZE = 200


def load_file(file_path: str):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()


def chunk_code(lines, chunk_size=CHUNK_SIZE):

    chunks = []
#Went with sliding window approach to preserve context across chunks. Can be optimized later.
    for i in range(0, len(lines), chunk_size):
        chunk = "".join(lines[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def load_and_chunk_files(file_paths):

    all_chunks = []

    for file_path in file_paths:

        try:
            lines = load_file(file_path)

            chunks = chunk_code(lines)

            for chunk in chunks:

                all_chunks.append({
                    "file_path": file_path,
                    "content": chunk
                })

        except Exception as e:

            print(f"Skipping {file_path}: {e}")

    return all_chunks