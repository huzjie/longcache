"""协议转换单测。"""
from longcache.protocol.codec import PromptCodec, Message


def test_encode_decode():
    codec = PromptCodec()
    msgs = [Message("user", "你好"), Message("assistant", "你好，有什么可以帮你？")]
    raw = codec.encode(msgs)
    back = codec.decode(raw)
    assert len(back) >= 1
    assert back[0].role == "user"
