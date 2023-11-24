"""
MIT License

Copyright (c) 2023-present qvco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from ..config import Endpoints
from ..models import ChatRoom, GifImageCategory, Message, StickerPack
from ..responses import (
    ChatRoomResponse,
    ChatRoomsResponse,
    TotalChatRequestResponse,
    CreateChatRoomResponse,
    FollowUsersResponse,
    GifsDataResponse,
    MessageResponse,
    MessagesResponse,
    StickerPacksResponse,
    UnreadStatusResponse,
)


def accept_chat_requests(self, chat_room_ids: list[int], access_token: str = None):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/accept_chat_request",
        payload={"chat_room_ids[]": chat_room_ids},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Accepted chat requests.")
    return response


def check_unread_status(
    self, from_time: int, access_token: str = None
) -> UnreadStatusResponse:
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/unread_status",
        params={"from_time": from_time},
        data_type=UnreadStatusResponse,
        auth_required=True,
        access_token=access_token,
    )


def create_group_chat(
    self,
    name: str,
    with_user_ids: list[int],
    icon_filename: str = None,
    background_filename: str = None,
    access_token: str = None,
) -> CreateChatRoomResponse:
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/new",
        payload={
            "name": name,
            "with_user_ids[]": with_user_ids,
            "icon_filename": icon_filename,
            "background_filename": background_filename,
        },
        data_type=CreateChatRoomResponse,
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Group chat '{name}' has been created.")
    return response


def create_private_chat(
    self,
    with_user_id: int,
    matching_id: int = None,
    hima_chat: bool = False,
    access_token: str = None,
) -> CreateChatRoomResponse:
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/new",
        payload={
            "with_user_id": with_user_id,
            "matching_id": matching_id,
            "hima_chat": hima_chat,
        },
        data_type=CreateChatRoomResponse,
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Created a private chatroom with '{with_user_id}'.")
    return response


def delete_background(self, room_id: int, access_token: str = None):
    response = self.request(
        "DELETE",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{room_id}/background",
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Background image of the chatroom has been deleted.")
    return response


def delete_message(self, room_id: int, message_id: int, access_token: str = None):
    response = self.request(
        "DELETE",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{room_id}/messages/{message_id}/delete",
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Message has been deleted.")
    return response


def edit_chat_room(
    self,
    chat_room_id: int,
    name: str,
    icon_filename: str = None,
    background_filename: str = None,
    access_token: str = None,
):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{chat_room_id}/edit",
        payload={
            "name": name,
            "icon_filename": icon_filename,
            "background_filename": background_filename,
        },
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Chatroom has been updated.")
    return response


def get_chatable_users(
    self,
    # @Body @Nullable SearchUsersRequest searchUsersRequest
    from_follow_id: int = None,
    from_timestamp: int = None,
    order_by: str = None,
    access_token: str = None,
) -> FollowUsersResponse:
    return self.request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/followings/chatable",
        payload={
            "from_follow_id": from_follow_id,
            "from_timestamp": from_timestamp,
            "order_by": order_by,
        },
        data_type=FollowUsersResponse,
        auth_required=True,
        access_token=access_token,
    )


def get_gifs_data(self, access_token: str = None) -> list[GifImageCategory]:
    return self.request(
        "GET",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        data_type=GifsDataResponse,
        auth_required=True,
        access_token=access_token,
    ).gif_categories


def get_hidden_chat_rooms(
    self, access_token: str = None, **params
) -> ChatRoomsResponse:
    """

    Parameters:
    ---------------

        - from_timestamp: int - (optional)
        - number: int - (optional)

    """
    return self.request(
        "GET",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        params=params,
        data_type=ChatRoomsResponse,
        auth_required=True,
        access_token=access_token,
    )


def get_main_chat_rooms(
    self, from_timestamp: int = None, access_token: str = None
) -> ChatRoomsResponse:
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/main_list",
        params=params,
        data_type=ChatRoomsResponse,
        auth_required=True,
        access_token=access_token,
    )


def get_messages(
    self, chat_room_id: int, access_token: str = None, **params
) -> list[Message]:
    """

    Parameters:
    ---------------
        - from_message_id: int - (optional)
        - to_message_id: int - (optional)

    """
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/messages",
        params=params,
        data_type=MessagesResponse,
        auth_required=True,
        access_token=access_token,
    ).messages


def get_request_chat_rooms(
    self, access_token: str = None, **params
) -> ChatRoomsResponse:
    """

    Parameters:
    ----------

        - number: int (optional)
        - from_timestamp: int (optional)
        - access_token: str (optional)

    """
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/request_list",
        params=params,
        data_type=ChatRoomsResponse,
        auth_required=True,
        access_token=access_token,
    )


def get_chat_room(self, chat_room_id: int, access_token: str = None) -> ChatRoom:
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}",
        data_type=ChatRoomResponse,
        auth_required=True,
        access_token=access_token,
    ).chat


def get_sticker_packs(self, access_token: str = None) -> list[StickerPack]:
    return self.request(
        "GET",
        endpoint=Endpoints.STICKER_PACKS_V2,
        data_type=StickerPacksResponse,
        auth_required=True,
        access_token=access_token,
    ).sticker_packs


def get_total_chat_requests(self, access_token: str = None) -> int:
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/total_chat_request",
        data_type=TotalChatRequestResponse,
        auth_required=True,
        access_token=access_token,
    ).total


def hide_chat(self, chat_room_id: int, access_token: str = None):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        payload={"chat_room_id": chat_room_id},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Chatroom '{chat_room_id}' has been hidden.")
    return response


def invite_to_chat(
    self, chat_room_id: int, user_ids: list[int], access_token: str = None
):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/invite",
        payload={"with_user_ids": user_ids},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Invited users to the chatroom.")
    return response


def kick_users_from_chat(
    self, chat_room_id: int, user_ids: list[int], access_token: str = None
):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/kick",
        payload={"with_user_ids[]": user_ids},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Users have been kicked from the chatroom.")
    return response


def pin_chat(self, room_id: int, access_token: str = None):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{room_id}/pinned",
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Pinned the chatroom.")
    return response


def read_message(self, chat_room_id: int, message_id: int, access_token: str = None):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/messages/{message_id}/read",
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Message has been read.")
    return response


def refresh_chat_rooms(
    self, from_time: int = None, access_token: str = None
) -> ChatRoomsResponse:
    params = {}
    if from_time:
        params["from_time"] = from_time
    return self.request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/update",
        params=params,
        data_type=ChatRoomsResponse,
        auth_required=True,
        access_token=access_token,
    )


def remove_chat_rooms(self, chat_room_ids: list[int], access_token: str = None):
    chat_room_ids = [chat_room_ids] if isinstance(chat_room_ids, int) else chat_room_ids
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/mass_destroy",
        payload={"chat_room_ids": chat_room_ids},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Chatrooms have been removed.")
    return response


def report_chat_room(
    self,
    chat_room_id: int,
    opponent_id: int,
    category_id: int,
    reason: str = None,
    screenshot_filename: str = None,
    screenshot_2_filename: str = None,
    screenshot_3_filename: str = None,
    screenshot_4_filename: str = None,
    access_token: str = None,
):
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/{chat_room_id}/report",
        payload={
            "chat_room_id": chat_room_id,
            "opponent_id": opponent_id,
            "category_id": category_id,
            "reason": reason,
            "screenshot_filename": screenshot_filename,
            "screenshot_2_filename": screenshot_2_filename,
            "screenshot_3_filename": screenshot_3_filename,
            "screenshot_4_filename": screenshot_4_filename,
        },
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info(f"Chatroom '{chat_room_id}' has been reported.")
    return response


def send_message(
    self, chat_room_id: int, access_token: str = None, **params
) -> MessageResponse:
    response = self.request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/{chat_room_id}/messages/new",
        payload=params,
        data_type=MessageResponse,
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Your message has been sent.")
    return response


def unhide_chat(self, chat_room_ids: int, access_token: str = None):
    response = self.request(
        "DELETE",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        params={"chat_room_ids": chat_room_ids},
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Unhid the chatrooms.")
    return response


def unpin_chat(self, chat_room_id: int, access_token: str = None):
    response = self.request(
        "DELETE",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{chat_room_id}/pinned",
        auth_required=True,
        access_token=access_token,
    )
    self.logger.info("Unpinned the chatroom.")
    return response
