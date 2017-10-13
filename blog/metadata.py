from rest_framework.metadata import SimpleMetadata


class BlogMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        if hasattr(view, "sample_response"):
            print("yeap")
            metadata['responses'] = {
                "200": {
                    "description": getattr(view, "smaple_response_title", "Example Successful Response Format"),
                    "examples": {
                        "application/json": [
                            getattr(view, "smaple_response")
                        ]
                    }
                }
            }
        else:
            print("nope")
        return metadata
