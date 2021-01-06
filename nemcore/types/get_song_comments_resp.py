from typing import Optional, List, Any

from .easy_access import EasyAccessDict


class AvatarDetail(EasyAccessDict):
    user_type: int
    identity_level: int
    identity_icon_url: str


class Experts(EasyAccessDict):
    the_1: str


class Associator(EasyAccessDict):
    vip_code: int
    rights: bool


class VipRights(EasyAccessDict):
    associator: Associator
    music_package: None
    red_vip_annual_count: int
    red_vip_level: int


class User(EasyAccessDict):
    location_info: Optional[str]
    live_info: None
    anonym: int
    user_id: int
    avatar_detail: Optional[AvatarDetail]
    user_type: int
    remark_name: None
    vip_rights: Optional[VipRights]
    nickname: str
    avatar_url: str
    auth_status: int
    expert_tags: None
    experts: Optional[Experts]
    vip_type: int


class BeReplied(EasyAccessDict):
    user: User
    be_replied_comment_id: int
    content: str
    status: int
    expression_url: None


class CommentDecoration(EasyAccessDict):
    bubble_id: Optional[int]


class PendantData(EasyAccessDict):
    id: int
    image_url: str


class Comment(EasyAccessDict):
    user: User
    be_replied: List[BeReplied]
    pendant_data: Optional[PendantData]
    show_floor_comment: None
    status: int
    comment_id: int
    content: str
    time: int
    liked_count: int
    expression_url: None
    comment_location_type: int
    parent_comment_id: int
    decoration: Optional[CommentDecoration]
    replied_mark: None
    liked: bool


class HotCommentDecoration(EasyAccessDict):
    pass


class HotComment(EasyAccessDict):
    user: User
    be_replied: List[BeReplied]
    pendant_data: Optional[PendantData]
    show_floor_comment: None
    status: int
    comment_id: int
    content: str
    time: int
    liked_count: int
    expression_url: None
    comment_location_type: int
    parent_comment_id: int
    decoration: HotCommentDecoration
    replied_mark: None
    liked: bool


class GetSongCommentsResp(EasyAccessDict):
    is_musician: bool
    cnum: int
    user_id: int
    top_comments: List[Any]
    more_hot: bool
    hot_comments: List[HotComment]
    comment_banner: None
    code: int
    comments: List[Comment]
    total: int
    more: bool
