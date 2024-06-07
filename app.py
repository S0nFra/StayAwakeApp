try:
    from PIL import Image
    from plyer import notification as npa
    from threading import Thread, Event
    from pystray import Icon, MenuItem
    import os
    import pyautogui
    import time
    from datetime import datetime
    from random import randint
    from dotmap import DotMap
    import base64
    import numpy as np
    import cv2
    import io
except Exception as exp:
    print (f'Error: {exp}')
    exit()
    
WAIT_TIME = 60 # s
encoded_icons = DotMap({
   "alarm_clock_on_action":"iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAxnpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDsMgDPvnFDsCiQOF49C1k3aDHX+mhKndZimPxpVjEvbX8xFuHSoWLC0l15wjYdWqNjYlDrQjS7QjT6hPL/PwIZQjsGIQJY8qcz6FvEpjl05C5e7EeiWq+fryJeSL0B11C5sLVReCDkJcoI1nxVzLcn7CuscryojQ0+qqh6P4+20Lr7cl7oHqDkFkBvIwgB4IaCSEWWH8UZDYg2RjVHfCg/y700R4AzhFWcgGf9OAAAABhGlDQ1BJQ0MgcHJvZmlsZQAAeJx9kT1Iw0AcxV9TpaJVBzsU6ZChOtlFRRylikWwUNoKrTqYXPoFTRqSFBdHwbXg4Mdi1cHFWVcHV0EQ/ABxdXFSdJES/5cUWsR4cNyPd/ced+8AoVllqtkzB6iaZaQTcTGXXxUDrxhAGEOIICYxU09mFrPwHF/38PH1LsazvM/9OQaVgskAn0g8x3TDIt4gntm0dM77xCFWlhTic+IJgy5I/Mh12eU3ziWHBZ4ZMrLpeeIQsVjqYrmLWdlQiaeJo4qqUb6Qc1nhvMVZrdZZ+578hcGCtpLhOs0IElhCEimIkFFHBVVYiNGqkWIiTftxD/+o40+RSyZXBYwcC6hBheT4wf/gd7dmcWrSTQrGgd4X2/4YAwK7QKth29/Htt06AfzPwJXW8deawOwn6Y2OFj0ChreBi+uOJu8BlztA+EmXDMmR/DSFYhF4P6NvygMjt0D/mttbex+nD0CWulq+AQ4OgfESZa97vLuvu7d/z7T7+wHsH3LXN/e+QwAADlVpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDQuNC4wLUV4aXYyIj4KIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6Mjg0ODhiYTUtMzRkMS00NDM1LThmNjMtZDY1MDc5NGRkYjc2IgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjM3YTJmNmYxLTM3ZmMtNDAxZC1iZWFkLWFjMzAyNzE2OWYzZCIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmRmYWE2ZTExLWMzMDItNGE4Zi04NGE3LTI2ODZjYzA0NGQ2OSIKICAgZGM6Rm9ybWF0PSJpbWFnZS9wbmciCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IldpbmRvd3MiCiAgIEdJTVA6VGltZVN0YW1wPSIxNzAwODM2MjEyNzQxNjU3IgogICBHSU1QOlZlcnNpb249IjIuMTAuMzYiCiAgIHRpZmY6T3JpZW50YXRpb249IjEiCiAgIHhtcDpDcmVhdG9yVG9vbD0iR0lNUCAyLjEwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDIzOjExOjI0VDE1OjMwOjA5KzAxOjAwIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyMzoxMToyNFQxNTozMDowOSswMTowMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjYyOWI5ZmRmLTI0Y2ItNDFjMy05NzQ0LTk3OTI0M2I0ZDM0MiIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyMy0xMS0yNFQxMToxNzozNyIvPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDphNjgyNDlkNy0yYzEwLTQ0NjgtYTE0OS1mNDg4NmU4OGNlY2EiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjMtMTEtMjRUMTU6MzA6MTIiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+tAxcYAAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+cLGA4eDPKBkQUAAA8sSURBVHja7d2LdSpLEgTAARfw30TZgCzgDAJNfzIjTGCqsrP7at8eBwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJy7+Ql6PH+O51tD8TAXYP9RAKhYemEA9t/+KwBYfCEAMkAGKAA0L74QAPtv/xUAipdfCID9t/8KAKXLLwTA/tv/HHc/geUHkDVeALCQbgEgA2SAAoDFFwAgA2RAIv8EYPEBZJACgMUDkEUNPN9YuO8GyBMgyAJZ4AUAbRuQTSgAWDBARqEAYLEAWYUCgIUCZBYKABYJkF0oAFggQIahAFgcAFmGAmBhAGQaCoBFAZBtKAAWBKiw2399T8YpAIQshv/0J6AEKABYCACZt9Mlzk9gEdz+QY7IES8AWFoAGegFAIOvtYNMkSkKABbVooJskS0KABYUkDEyRgHAYgKyRtYoAFhIQObIHAXAIlpEQPbIHgXAAlpAQAbJIAXA4lk8QBbJIgXAwlk4QCbJJAXAolk0QDahAFgwCwbIKBQAi2WxAFmFAmChLBQgs1AALJJFAmQXCoAFskCADEMBsDiALJNlCgAWBpBpMk0BwKIAsk22KQBYEEDGyTgFwGJYDEDWyToFwEJYCEDmyTwFwCJYBED2yT4FwAJYANJn0ryZNzOpABh8g0/p3JlJM2nuFAADb+ApPejNq3k1YwqAQTfoOOzNsTk2UwqAATfg5gizbbbNkQJgsA222cG8m3ezowAYaANtZjD/5t/MKACG2SCbEeyEnTAjCoAhNsRmAztiR8yGAmCADa95wM7YGfOgABhcHPrYITtkDhSA6KEVXEIL+2SffH8FoGxghZVDH/tlv3xzBaBsWIWTgx+7Ztd8awWgbFAFkkMfe2f3fGMFoGxIhZCDH3toD31XBaBsQIWOgx87aSd9TwWgbDgFjYMfRcB++o4KQNlgChcHP4qAXfX9FICyoRQoDn4UAXvruykAZQMpRBz8KAJ22PdSAMqGUXA4+FEE7LPvpACUDaOwcPijBNhr30cBKBtEQ+jgRxGw476LAlA2iAbQwY8iYN9l7yx3P4EwcPiD2ZaFXgAsqIEXjiAD5K8CYAgNn4Mf5IH8VQAMoeFz+INckL8KgCE0fA5+kBHyVwEwiAbP4Q/yQv4qAN2DaPAc/ODgkr8KAJaXZQ8Z30cJQAEAh78Dwvf1jVEAwMHgADAD5gAFAAS/kDcf5gMFAIS7QDczZgYFACEuxIW3WTJLKAAIbIS0+TJfKAAIZ6GMeTNvKAAIYyGM+TN/KAAIXqGLmTSTKAAIWiGL+TSfKAAIV6GKeTWvKAAIU0GK2TW7KAAIUOGJOTbHKAAITWGJmTbXKAAISgGJGTfjKAAIRqGIEgAKAA5/MPcoAJAeggIQO2AHUAAoCj6hh32wDygAFIWdoMNu2A0UAAQc2BE7ggJAarAJNeyLfUEBoCjMBBl2x+6gACDAwA7ZIRQAUoNLaGGf7BMKAMIK7JW9QgEgNaQEFPbLjqEA4PAHu2bXUAAQSGDn7BzvuvsJWD2EBBEOT/ACQNFNRIhiB+0gCgCCB+yiXUQBQOCAnbSTKABEBI2QwW7aT8bxR4AIFxg452YdLwC4YTj8l5sP38Kumg8FAIEiUMrnwrexs+ZCAUCQCJLimfCd7K6ZyORvABAgDpW4A8ougBcAYS/wzIPvZo/NAwqA0BAa5sH3s8/mAQVAWAgL8+A72mvzUMrfACAkHBrRB5RdAQVA4As0s4CdMX8oAAJfkCH07Y55UADA4Q92iKb58hO4eQku8+A7+87mwQsAQkAIgJ2KzigUABz+YLdQANCsBRTYMa8ACgAAoACgUbv9g13zCqAAYJEc/mDnlAAFAEEE2D0UAEoatAACO+gVQAFA8ACgAKA5A8q4LFMAiFoYt3+wk0qAAoCgAewmCgDJTVnAAF4BFAAAlHQUANz+AbvqFUABQKAAdhYFAM0YQNYpALhJAHYXBYBVG7EAAbwCKAAAeAVAAcDtH1ACvAIoAACAAoDbP2CnvQIoAAgKwG6jAAAACkCpFZ++3BDAK4AsVAAAAAUAt3/AK4BXAAUAAFAAcPsHvAJ4BVAAEAQAKAAAKP8oAMVWe+ISAICMVAAA8AqAAoBmCyArFQA0f0AWoAAAAAoAJ/zxH+AVYN/MVAAAAAUATR+QDSgAvOApC0B2KgBo+ICMQAEAABSAOJ6wAGSoAsBUnvYAWYECAAAKABo9gMxQAPgX/u0KQJYqAACAAsA4nvIA2YECMIgnKwCZqgAAAAoA43jCA2QICgAAoABcxb9VAchWBYBpPN0BsgQFAABQAABAAeDf+DcqABmrADCNf7MDZAoKAACgAAAACgAAKAB8bpU/TvFvdUBytvhDQAUAAFAAAAAFAABQAFr4939AxqAAAAAKwJX8VSqAzFUAAAAFAABQALiIP84BQAEAwGUDBQAAUAAAQAHwEwCAAsAf+d+jAsheBQAAUAAYw1/lAqAAAODSgQIAACgAAIACAAAKAACgAAAACgAAoAAAAAoAAKAAAAAKAACgAADf8/+GBigA4PAHUAAAAAUA3P4BFABw+AMoAACgALCb2+O4+RXc/gEUAIcCvjOAAgAAKADg9g+gAIDDH1AAAN7mD1BBAQDc/gEFAEg//N3+QQEAABQAwO0fUAAAhz+gAAAACgDg9g8oAODwd/gDCgAAoACA27/bP2YWBQDL6Ns5/AEFAABQANyQcPs328heFABw+AtXQAEAAAXATwBu/27/oAAADn/YdoZRACwlACgAoKS5/QMKADj8Hf6gACA8AWSuAgC4/QMKAA4aHP4gYxQAAEABANz+AQUAcPiD2VUADKWDB1BqUQBAUCqrgAIADn+HP6AAAAAKALm3UL+72z9m2wwrAFEMp4A0m4ACAAAoAOD27/YPKACUH0p+Z4c/ZhwFIIrABZCtCgC4GQlMQAHAAeW3dfhjzlEAAAAFIIfbl1uR+QMzrQDgsPJ7CkrMOgoAAKAAxHITcyMyc2CuFQAcXH5DIYl5RwEAABQANHq/nds/5h0FIIdgFoZmDMy3AgAAKAC4zfq93I4w8ygAsYS0IDRXYMYVABxsgGxAAQBB6GYETMoSP0HnoeIQcfiDfPICAAAoAOAW5PYPKABEhrc/+DE/sGIWmHUFAAC4smz5CbRtX2XtFxHfCHmEFwBoa+gCEVAAaLv5AnYfBcCNThCYFQjeefOuAADCEFAAhLtXAMDtHwUAFEQABUDIewUwF+D2jwIAACgAeAVw+we7zcvM8RNYSofR/G/h8EfO4AUAAPACoJ1r5+nfwi0I+YIXAGhr4EIQUAAcAm4OvgW4/aMAIEDCw0kIYndRAHAYlH0P3xu7hQKAm0RZUAlA7CxLZJyfwOI6uMZ8Ewc/MsQOeAFAsGz2EvBtcAk+7CheANDgS76R3wrZYR8UAKJavEUGuSEz9uefACxLXEEBhz8oAEoAgCxDAcCNA+wiHIe/AbDc2j3IB/ngBQDcPsDu4QUAi67pg0yQCQoAFt7CgyyQBSn8EwAAeAFA89f8QQbIAC8AEBhQYLcc/igAW9lluZQAsFNscKb4CYSB2wDYd/vuBQDcWsAO4QUAweBmAHbcjisACAgBAXbbbkfwTwAINLArDn8FgJ3stnxKANgRFjpD/ARCQ3EBe2yPFQCEh/AA+2t/C/gnAAQe2AW8ACBI3CTAztpZBQCBIlDArtpVBQDBIljAjqIAIFyEDBTspr3M5I8AE1vdxsvqD6Jw+IMXALwEgF20iygACB6wg3YQBQABBHbP7qEAkBlCwgg7Z99QAFACzCt2zZ6hANBYAgQU9st+oQAgpMBe2SsUAIQV2Cf7hAJARWgJLuyQHUIBQICB3bE7KAC0BZkww77YFxQAikNNsGFH7AgKAAIO7IbdQAGgLeiEHfbBPqAAUBx6gg87YAdQACgOQCGIuQcFAGEI5h0FANpCUTBixlEAoDgghaSZNtcoAFAemELTHJtjFAAoDk8BanbNLgoAFAepMDWv5hUFAIpDVbiaT7OJAoCQLS8BwtZMmkcUAIQuwtf8mT8UAISwMLZT5s28oQAglIUz5st8oQAgpAW2X8EsmSMUAIS3ILd/ZsbMoAAg0IV7xz6aD/OBAoCQJzz0zYE5QAFAESD0UPCNHfwoAOCA2PRg8Y0c/igAoASAgx8FABQBcPijAIASAA5/FABQBMDBjwIASgA4+FEAQBEAhz8KACgCOPhlLgoAKAE4/EEBAEUABz8oAKAI4OAHBQAlQAnAwQ8KAIoAOPxBAUARAAc/KAAoAuDgBwUARQAc/KAAoAiAgx8UAC44XFcISUWAtIN/p/1DAcCNWhnAoV++fygAlB38K4aQIkDrvCoCKABMPSgVARz89g8FgLLDf9UQUgYc+vYPBQCH/6DDcMUQUgQc/PYPBQCHf3kAKQMOfTuIAoDDvzyAlAGHvh1EAcDhXx5AyoBD3w6iAODwFz4KgQPfHqIAIHTag0cZMDt2EQUAgSN4FAJzYhdRABA4QkchMBP2EQUAYSNwlALf306iANB+2AibjmLgO9tLFACEjKBxaGA3UQBov00KGeyn/WSOu59AuADIEAUAiwsgSxQALCwgU2SKAoBFBWQLCgAWFPic/+MiFAAqF9NfGIOsQQHAQgIyh5GXMD+BRXT7B3tsj70AIDQAZJAXACyeWwPYaTutACAoBAXYbbutACAgBATYcTuuACAYBAPYdbuuACAQBALYeRQABAFg91EAEACADEABwOIDsgAFAAsPyAQUAItu0QHZgAJgwS04yAgZgQJgsS02yApZgQJgoS00yAyZwRn/b4BYZLB7eAFAkxdAID/khxcAsLxgF/ECgPYucECWyBIvALhtAHYTBQABA9hRFAAEC2BXUQAQKICdRQFAkAB2FwUAAQLYYRQABAdgl1EAEBiAnUYBQFAAdhsFAAEB2HEUAAQDYNc5nwU/wXyz/xveAgHkjtzxAoDbAGD38QJAchsXAIDs8QKA9g/IArwAkNzELTwgf/AhypbQ8gHyBwWgbAktHyB/UADKltDyAfIHBaBoES0eIH9QAIoW0eIB8gcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD41i+nBC2l7uVgbAAAAABJRU5ErkJggg==",
   "alarm_clock":"iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAxHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDsMwCPvPKXYEwDSP46RrJ+0GO/5IIVO7zVIMwZEhpP31fKTbgLAmXUrNLWcyaNMm3ZJKjn4wkx48IVG91NNHECvBIlyo2SPP+jSKyN2y5WRU7yGsV6FptK9fRtEIY6IxwhZGLYwgLnAYdP8W5VbL+QvrTldUP2nQGq7HRPR712Lb2xbrA5EdDDIGsg+AcZDQTWBjgdpDzxnFGCgxiS3k354m0hs4hVnK+Y5o6QAAAYVpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfW6VSKx3sUMQhQxUEu6iIY6liESyUtkKrDiaXfkGThiTFxVFwLTj4sVh1cHHW1cFVEAQ/QFxdnBRdpMT/JYUWMR4c9+PdvcfdO8DbqjHF6IsDimrqmWRCyBdWBf8rBhFBACFMiMzQUtnFHFzH1z08fL2L8Sz3c3+OIbloMMAjEMeZppvEG8Szm6bGeZ84zCqiTHxOPKnTBYkfuS45/Ma5bLOXZ4b1XGaeOEwslHtY6mFW0RXiGeKorKiU7807LHPe4qzUGqxzT/7CYFFdyXKd5iiSWEIKaQiQ0EAVNZiI0aqSYiBD+wkX/4jtT5NLIlcVjBwLqEOBaPvB/+B3t0ZpespJCiaA/hfL+hgD/LtAu2lZ38eW1T4BfM/Aldr111vA3Cfpza4WPQJC28DFdVeT9oDLHSDypIm6aEs+mt5SCXg/o28qAMO3QGDN6a2zj9MHIEddLd8AB4fAeJmy113ePdDb279nOv39ALe0csIzqNo6AAANdmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDoyODQ4OGJhNS0zNGQxLTQ0MzUtOGY2My1kNjUwNzk0ZGRiNzYiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ZDZhNWMzZTgtODhjNy00ZTVmLWFiY2ItYTAwNjAwMzQ3MmFlIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZGZhYTZlMTEtYzMwMi00YThmLTg0YTctMjY4NmNjMDQ0ZDY5IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE3MDA4MjEwNTcyNzQ3NzkiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zNiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjM6MTE6MjRUMTE6MTc6MzcrMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIzOjExOjI0VDExOjE3OjM3KzAxOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NjI5YjlmZGYtMjRjYi00MWMzLTk3NDQtOTc5MjQzYjRkMzQyIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDIzLTExLTI0VDExOjE3OjM3Ii8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/Pup/Va0AAAAGYktHRAAAAAAAAPlDu38AAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAHdElNRQfnCxgKESUwor16AAAPKUlEQVR42u3di5XrOhIDQEv55+yJwMcey+IHqArB6gZB3tm3jwcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC8d/gJejyfz+dHQ3Ec5gLsPwoADUsvDMD+238FAIsvBEAGyAAFgObFFwJg/+2/AkDx8gsBsP/2XwGgdPmFANh/+5/j9BNYfgBZ4wUAC+kWADJABigAWHwBADJABiTyTwAWH0AGKQBYPABZ1MDzjYW7NkCeAEEWyAIvAGjbgGxCAcCCATIKBQCLBcgqFAAsFCCzUACwSIDsQgHAAgEyDAXA4gDIMhQACwMg01AALAqAbEMBsCBAhd3+63syTgEgZDH8pz8BJUABwEIAyLydLnF+Aovg9g9yRI54AcDSAshALwAYfK0dZIpMUQCwqBYV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",
   "zzz_sleep_symbol":"iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAAwnpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBRDsMgCP3nFDuC8qjicezaJbvBjj8suLTNXiLge+YJ0P55v+gxwFlIlqqllZIM0qRxt0KTox8xJzniBAd74eknsFGwDBe0eM6Tn0aRc7dqORnpM4T1KjSJ7/VmFB9hdDRa2MKohRHYhRwG3cdKpWk9j7Du6Qr1QyOg+njT5H6XatvbFiPBvCMjWQSKN4BxQOgmZIsMsYdeC/Tg505sIf/2NEFf3LBZEXrTA2IAAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1NFqRUHOxRxyFCdLIiKOJYqFsFCaSu06mBy6Rc0aUhSXBwF14KDH4tVBxdnXR1cBUHwA8TVxUnRRUr8X1JoEePBcT/e3XvcvQOEZpWpZk8MUDXLSCfiYi6/Kva9YgBhBDAJv8RMPZlZzMJzfN3Dx9e7KM/yPvfnGFQKJgN8InGM6YZFvEE8u2npnPeJQ6wsKcTnxBMGXZD4keuyy2+cSw4LPDNkZNPzxCFisdTFchezsqESzxBHFFWjfCHnssJ5i7NarbP2PfkLgwVtJcN1mqNIYAlJpCBCRh0VVGEhSqtGiok07cc9/COOP0UumVwVMHIsoAYVkuMH/4Pf3ZrF6Sk3KRgHel9s+2MM6NsFWg3b/j627dYJ4H8GrrSOv9YE5j5Jb3S0yBEwtA1cXHc0eQ+43AHCT7pkSI7kpykUi8D7GX1THhi+BQJrbm/tfZw+AFnqavkGODgExkuUve7x7v7u3v490+7vB6uFcr0g9iqjAAANdmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDphYjE2NGUyYS02N2EyLTRlYzctOGYwNy0xODkyMjkwNzQ5NDQiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ZTQ0MzljNTEtNGJhMC00YzE0LTgxZjctMTE4M2Q2MzgyYjZiIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6OThhNTk1NmMtZGY4MC00YmY0LTg5ZTYtMTJmNDY0MjljOTU4IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE3MDA4MjI4OTAyOTY0MTgiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zNiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjM6MTE6MjRUMTE6NDg6MTArMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIzOjExOjI0VDExOjQ4OjEwKzAxOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MjViNWQ1ZTAtZWUwMi00MjRkLTkwYmYtNmQzYjE0ZmM1N2Q3IgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDIzLTExLTI0VDExOjQ4OjEwIi8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PrJUxi4AAAAGYktHRAAAAAAAAPlDu38AAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfnCxgKMAoX7JXAAAAJQklEQVR42u3c0ZFjNxAEQWL99xn8Wg8YMQAq0wRKp+qB4t3nAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAby08A/NLee/sVuCKAa6Ub+OdfAQAwAAAAAwAAMAAAAAMAADAAAAADAAAwAAAAAwAAMAAAAAMAADAAAAADAAAwAAAAAwAAMAAAAAMAADAAAMAAAAAMAADAAAAADAAAwAAAAAwAAMAAAAAMAADAAAAADAAAwAAAAAwAAMAAAAAMAADAAAAADAAAwAAAAAMAADAAAAADAAAwAAAAAwAAMAAAAAMAADjM8hMA8G/vvTMBXCvd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"
})

def stringToRGB(base64_string, color_code=None):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata))
    if color_code is not None:
      return cv2.cvtColor(np.array(img), color_code)
    return img

def resource_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

class StayAwakeApp():
    
    def __init__(self, action_to_wake=None) -> None:
        self._sleep_img = stringToRGB(encoded_icons.zzz_sleep_symbol)
        self._allarm_img = stringToRGB(encoded_icons.alarm_clock)
        self._on_action_img = stringToRGB(encoded_icons.alarm_clock_on_action)
    
        pyautogui.FAILSAFE = False
        self._current_location = pyautogui.position()
        
        self._action_flag = Event()
        self._thread = Thread(target=self._thread_task, 
                              args=(
                                  self._action_flag,
                                  action_to_wake if action_to_wake else self._do_move,
                                ),
                              daemon=True
                            )

        self._app = Icon("StayAwake", self._sleep_img, menu=self._generate_menu())
        
    def _generate_menu(self):
        toggle_item = MenuItem(
                'Activate' if not self._action_flag.is_set() else "Deactivate",
                self._on_click,
                visible= self._action_flag
            )
        close_item = MenuItem(
                'Close',
                action= lambda : self.stop()
            )
        return [
            toggle_item,
            close_item
        ]
    
    def _on_click(self):
        if not self._action_flag.is_set():
            self._app.icon = self._allarm_img
            self._action_flag.set()
        else:
            self._app.icon = self._sleep_img
            self._action_flag.clear()
        self._app.menu = self._generate_menu()
        
    def _thread_task(self, flag:Event, action_to_wake):
        print(">> Thread started <<")
        try:
            while True:
                if flag.is_set():
                    print('>> Checking')
                    if self._current_location == pyautogui.position():
                        print(">> No manual movement detected >> Triggering stay-awake")
                        self._app.icon = self._on_action_img
                        action_to_wake()
                        self._app.icon = self._allarm_img
                    else:
                        current_location = pyautogui.position()
                        print(f'>> Mouse manually moved from {self._current_location} to {current_location} >> No stay-awake triggered')
                        self._current_location = current_location
                else:
                    pass
                time.sleep(WAIT_TIME)
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def _has_moved(self, currentLocation):
        try:
            time.sleep(randint(0,2))
            if pyautogui.position() == currentLocation:
                return False
            else:
                print('>> Input detected, interrupting stay-awake')
                return True
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def _do_move(self):
        try:
            print(f'>> Moving at {self._current_location}')
            for n_move in range(1, randint(2,4)):
                if self._has_moved(self._current_location):break
                pyautogui.moveTo(self._current_location[0] + n_move, self._current_location[1] + n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] - n_move, self._current_location[1] - n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] - n_move, self._current_location[1] + n_move)
                pyautogui.moveTo(self._current_location)
                if self._has_moved(self._current_location): break
                pyautogui.moveTo(self._current_location[0] + n_move, self._current_location[1] - n_move)
                pyautogui.moveTo(self._current_location)
            print(f'>> Made movement at {datetime.now().time()}')
        except Exception as exp:
            print(f'>> Error: {exp}')
            exit()
    
    def run(self):
        self._thread.start()
        self._app.run()
    
    def stop(self):
        self._app.stop()

def press_key(key='ctrlleft'):
    pyautogui.press(key)
    time.sleep(1)
    pyautogui.press(key)

if __name__ == "__main__":
    from tendo import singleton
    try:
        me = singleton.SingleInstance()
    except:
        exit()
    StayAwakeApp(press_key).run()
