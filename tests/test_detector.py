from detector import message_obj_has_image, raw_message_has_image


class M:
    def __init__(self, message=None, raw_message=None):
        self.message = message
        self.raw_message = raw_message


def test_chain_image():
    assert message_obj_has_image(M(message=[{"type": "image"}]))


def test_raw_list_image():
    assert raw_message_has_image([{"type": "image", "data": {}}])


def test_cq_image_string():
    assert raw_message_has_image("[CQ:image,file=abc]")


def test_no_image():
    assert not raw_message_has_image("hello")


def test_abnormal_structure():
    assert not raw_message_has_image({"x": 1})
