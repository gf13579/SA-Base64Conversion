import sys
import import_declare_test
import base64

from splunklib.searchcommands import \
    dispatch, StreamingCommand, Configuration, Option, validators

def stream(streaming_command: StreamingCommand, events):

    for event in events:
        if streaming_command.action == "decode":
            try:
                # Ensure the field content is a string before encoding to bytes for b64decode
                content_to_decode = event[str(streaming_command.field)]
                if isinstance(content_to_decode, str):
                    event["decoded_content"] = base64.b64decode(content_to_decode).decode("utf-8")
                else:
                    # Handle cases where the content might not be a string (e.g., bytes already)
                    event["decoded_content"] = base64.b64decode(content_to_decode).decode("utf-8")
            except Exception as e:
                event["error"] = f"Decoding error: {e}"
        elif streaming_command.action == "encode":
            try:
                # Ensure the field content is a string before encoding to bytes for b64encode
                content_to_encode = event[str(streaming_command.field)]
                if isinstance(content_to_encode, str):
                    event["encoded_content"] = base64.b64encode(content_to_encode.encode("utf-8")).decode("utf-8")
                elif isinstance(content_to_encode, bytes):
                    # If it's already bytes, just encode it
                    event["encoded_content"] = base64.b64encode(content_to_encode).decode("utf-8")
                else:
                    # Convert other types to string before encoding
                    event["encoded_content"] = base64.b64encode(str(content_to_encode).encode("utf-8")).decode("utf-8")
            except Exception as e:
                event["error"] = f"Encoding error: {e}"
        yield event
