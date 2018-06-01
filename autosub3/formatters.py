import json

import pysrt


class BaseFormatter(object):
    def generate(self, subtitles, show_before=0, show_after=0, *args, **kwargs) -> str:
        raise NotImplementedError()


class SRTFormatter(BaseFormatter):
    def generate(self, subtitles, show_before=0, show_after=0, *args, **kwargs) -> str:
        sub_rip_file = pysrt.SubRipFile()
        for i, ((start, end), text) in enumerate(subtitles, start=1):
            item = pysrt.SubRipItem()
            item.index = i
            item.text = str(text)
            item.start.seconds = max(0, start - show_before)
            item.end.seconds = end + show_after
            sub_rip_file.append(item)
        return '\n'.join(str(item) for item in sub_rip_file)


class VTTFormatter(BaseFormatter):
    def generate(self, subtitles, show_before=0, show_after=0, *args, **kwargs) -> str:
        formatter = SRTFormatter()
        text = formatter.generate(subtitles, show_before, show_after)
        text = 'WEBVTT\n\n' + text.replace(',', '.')
        return text


class JSONFormatter(BaseFormatter):
    def generate(self, subtitles, show_before=0, show_after=0, *args, **kwargs) -> str:
        raw_subtitles = [{
            'start': start,
            'end': end,
            'content': text
        } for ((start, end), text) in subtitles]
        return json.dumps(raw_subtitles, ensure_ascii=False)


class RawFormatter(BaseFormatter):
    def generate(self, subtitles, show_before=0, show_after=0, *args, **kwargs) -> str:
        return ' '.join(text for (_rng, text) in subtitles)


FORMATTERS = {
    'srt': SRTFormatter,
    'vtt': VTTFormatter,
    'json': JSONFormatter,
    'raw': RawFormatter,
}
