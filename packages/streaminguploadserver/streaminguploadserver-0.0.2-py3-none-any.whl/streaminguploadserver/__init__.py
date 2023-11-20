import http, os, pathlib, shutil, tempfile, uploadserver
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import DirectoryTarget, ValueTarget
from tqdm import tqdm

DEFAULT_CHUNK_SIZE = 65536
CONTENT_LENGTH_HEADER_NAME = "Content-Length"
FORM_ENCODING = "utf-8"
FILES_FORM_NAME = "files"

# Receive streaming uploads
def receive_streaming_upload(handler):
    assert hasattr(uploadserver.args, "allow_replace")
    assert (
        hasattr(uploadserver.args, "directory")
        and type(uploadserver.args.directory) is str
    )

    # Default return code is error
    return_code = (http.HTTPStatus.INTERNAL_SERVER_ERROR, "Server error")
    with tempfile.TemporaryDirectory() as temporary_directory:

        # Initialize parser and targets
        parser = StreamingFormDataParser(headers=handler.headers)
        directory_target = DirectoryTarget(temporary_directory)
        parser.register(FILES_FORM_NAME, directory_target)

        # Prepare upload processing
        total_size = int(handler.headers[CONTENT_LENGTH_HEADER_NAME])
        processed_size = 0
        current_chunk_size = DEFAULT_CHUNK_SIZE

        # Process upload in chunks
        with tqdm(
            desc="Receiving data from remote host",
            total=total_size,
            dynamic_ncols=True,
            mininterval=1,
            unit="B",
            unit_scale=True,
        ) as progress_bar:
            while processed_size < total_size:
                processed_size += current_chunk_size
                if processed_size > total_size:
                    current_chunk_size += total_size - processed_size
                chunk = handler.rfile.read(current_chunk_size)
                if chunk:
                    parser.data_received(chunk)
                    progress_bar.update(current_chunk_size)
                else:
                    handler.log_message("Upload was interrupted")
                    return (http.HTTPStatus.BAD_REQUEST, "Upload was interrupted")

        # Verify that a file was present
        if not (directory_target.multipart_filenames and all(multipart_filename for multipart_filename in directory_target.multipart_filenames)):
            return (http.HTTPStatus.BAD_REQUEST, 'No files selected')

        # Move temporary files to final destination
        source_directory_path = pathlib.Path(temporary_directory)
        destination_directory_path = pathlib.Path(uploadserver.args.directory)
        for multipart_filename in directory_target.multipart_filenames:
            source = source_directory_path / multipart_filename
            destination = destination_directory_path / multipart_filename
            if os.path.exists(destination) and not (uploadserver.args.allow_replace and os.path.isfile(destination)):
                destination = uploadserver.auto_rename(destination)
            shutil.move(source, destination)

        # Upload successful
        handler.log_message(
            "Upload of {} file(s) accepted".format(
                len(directory_target.multipart_filenames)
            )
        )
        return_code = (http.HTTPStatus.NO_CONTENT, None)

    return return_code


uploadserver.receive_upload = receive_streaming_upload


def main():
    uploadserver.main()
