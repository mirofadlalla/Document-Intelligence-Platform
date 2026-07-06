"""
PaddleOCR Engine
================

Lazy-loaded singleton for PaddleOCR.

The OCR engine is created only on the first request and then cached for
the lifetime of the application.

This keeps application startup fast while avoiding repeated model loading.
"""

from functools import lru_cache

from groq import Groq


# @lru_cache(maxsize=1)
# def get_ocr_engine():
#     """
#     Return a cached PaddleOCR instance.

#     Raises:
#         ImportError:
#             If PaddleOCR is not installed.

#         RuntimeError:
#             If the OCR engine cannot be initialized.
#     """

#     try:
#         from paddleocr import PaddleOCR
#     except ImportError as exc:
#         raise ImportError(
#             "PaddleOCR is not installed. "
#             "Install it with:\n"
#             "pip install paddlepaddle paddleocr"
#         ) from exc

#     try:
#         return PaddleOCR(
#             use_doc_orientation_classify=False,
#             use_doc_unwarping=False,
#             use_textline_orientation=False,
#         )
#     except Exception as exc:
#         raise RuntimeError(
#             "Failed to initialize PaddleOCR. "
#             "This is usually caused by incompatible versions of "
#             "paddlepaddle, paddleocr, or paddlex."
#         ) from exc


import base64

@lru_cache(maxsize=1)
def return_client():
  return Groq()

def extract_content_from_img(file_path : str):
  with open(file_path, "rb") as f:
    image = base64.b64encode(f.read()).decode()

  completion = return_client().chat.completions.create(
      model="qwen/qwen3.6-27b",
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "Extract all fields from this delivery slip."
                  },
                  {
                      "type": "image_url",
                      "image_url": {
                          "url": f"data:image/png;base64,{image}"
                      }
                  }
              ]
          }
      ],
      temperature=0,
      max_tokens=2048
  )

  return completion.choices[0].message.content