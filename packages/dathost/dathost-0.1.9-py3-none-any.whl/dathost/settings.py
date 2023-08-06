from __future__ import annotations

from .gamemodes import COMPETITIVE
from .map_source import MAP_GROUP

from .exceptions import (
    InvalidSlotSize,
    MultipleGames,
    InvalidTickrate,
    InvalidSteamID,
    InvalidStorageSize
)


VALID_TICKRATES = [
    64,
    85,
    100,
    102.4,
    128
]


class ServerSettings:
    __game = False

    def __init__(self, name: str, location: str,
                 custom_domain: str = None,
                 autostop: bool = False, autostop_minutes: int = 0,
                 mysql: bool = False, scheduled_commands: list = None,
                 user_data: str = None,
                 reboot_on_crash: bool = True,
                 max_disk_usage_gb: int = None,
                 manual_sort_order: int = None,
                 core_dump: bool = False) -> None:
        """Used to store settings on a server.

        Parameters
        ----------
        name : str
            Name of server.
        location : str
            Location of server.
        custom_domain : str, optional
            Custom domain name, by default None
        autostop : bool, optional
            If autostop is enabled, by default False
        autostop_minutes : int, optional
            How many minutes, by default 0
        mysql : bool, optional
            If myself is enabled, by default False
        scheduled_commands : list, optional
            List of scheduled commands, by default None
        user_data : str, optional
            User meta data, by default None
        reboot_on_crash : bool, optional
            by default True
        max_disk_usage_gb : int, optional
            by default None
        manual_sort_order : int, optional
            by default None
        core_dump : bool, optional
            by default False
        """

        self.payload = {
            "name": name,
            "location": location,
            "autostop": autostop,
            "autostop_minutes": autostop_minutes,
            "enable_mysql": mysql,
            "reboot_on_crash": reboot_on_crash,
            "enable_core_dump": core_dump
        }

        if custom_domain:
            self.payload["custom_domain"] = custom_domain
        if scheduled_commands:
            self.payload["scheduled_commands"] = scheduled_commands
        if user_data:
            self.payload["user_data"] = user_data
        if manual_sort_order is not None:
            self.payload["manual_sort_order"] = manual_sort_order
        if max_disk_usage_gb is not None:
            if max_disk_usage_gb > 100 or max_disk_usage_gb < 30:
                raise InvalidStorageSize()

            self.payload["max_disk_usage_gb"] = max_disk_usage_gb

    def csgo(self, slots: int = None, tickrate: int = None,
             game_token: str = None, rcon_password: str = None,
             game_mode: str = COMPETITIVE, autoload_configs: list = None,
             disable_bots: bool = False, workshop_start_map_id: int = None,
             csay_plugin: bool = False, gotv: bool = False,
             sourcemod: bool = False, insecure: bool = False,
             map_group: str = MAP_GROUP, start_map: str = None,
             password: str = None, pure: bool = True,
             admins: list = None, plugins: list = None, steam_key: str = None,
             workshop_id: int = None
             ) -> ServerSettings:
        """Used for configuring a CS: GO server.

        Parameters
        ----------
        slots : int
        game_token : str
        tickrate : int
        game_mode : str, optional
            by default COMPETITIVE
        autoload_configs : list, optional
            by default None
        disable_bots : bool, optional
            by default False
        csay_plugin : bool, optional
            by default False
        gotv : bool, optional
            by default False
        sourcemod : bool, optional
            by default False
        insecure : bool, optional
            by default False
        map_group : str, optional
            by default MAP_GROUP
        start_map : str, optional
            by default None
        password : str, optional
            by default None
        pure : bool, optional
            by default True
        rcon_password : str, optional
            by default None
        admins : list, optional
            by default None
        plugins : list, optional
            by default None
        steam_key : str, optional
            by default None
        workshop_id : int, optional
            by default None
        workshop_start_map_id : int, optional
            by default None

        Raises
        ------
        MultipleGames
            Raised when you attempt to create one server
            with multiple games.
        InvalidSlotSize
            Raised when slot size is below 5 or above 64.
        InvalidTickrate
            Raised when tickrate is invalid.

        Returns
        -------
        ServerSettings
        """

        if self.__game:
            raise MultipleGames()

        self.__game = True

        self.payload["game"] = "csgo"

        if autoload_configs:
            self.payload["csgo_settings.autoload_configs"] = autoload_configs
        if disable_bots:
            self.payload["csgo_settings.disable_bots"] = disable_bots
        if csay_plugin:
            self.payload["csgo_settings.enable_csay_plugin"] = \
                csay_plugin
        if gotv:
            self.payload["csgo_settings.enable_gotv"] = gotv
        if sourcemod:
            self.payload["csgo_settings.enable_sourcemod"] = sourcemod
        if game_mode:
            self.payload["csgo_settings.game_mode"] = game_mode
        if insecure:
            self.payload["csgo_settings.insecure"] = insecure
        if map_group:
            self.payload["csgo_settings.mapgroup"] = map_group
        if start_map:
            self.payload["csgo_settings.mapgroup_start_map"] = start_map
        if password:
            self.payload["csgo_settings.password"] = password
        if pure:
            self.payload["csgo_settings.pure_server"] = pure
        if rcon_password:
            self.payload["csgo_settings.rcon"] = rcon_password
        if slots:
            if slots < 5 or slots > 64:
                raise InvalidSlotSize()

            self.payload["csgo_settings.slots"] = slots
        if admins:
            self.payload["csgo_settings.sourcemod_admins"] = admins
        if plugins:
            self.payload["csgo_settings.sourcemod_plugins"] = plugins
        if game_token:
            self.payload["csgo_settings.steam_game_server_login_token"] \
                = game_token
        if tickrate:
            if tickrate not in VALID_TICKRATES:
                raise InvalidTickrate()
            self.payload["csgo_settings.tickrate"] = tickrate
        if steam_key:
            self.payload["csgo_settings.workshop_authkey"] = steam_key
        if workshop_id:
            self.payload["csgo_settings.workshop_id"] = workshop_id
        if workshop_start_map_id:
            self.payload["csgo_settings.workshop_start_map_id"] \
                = workshop_start_map_id

        return self

    def mumble(self, slots: int = None, superuser_password: str = None,
               password: str = None, motd: str = None) -> ServerSettings:
        """Used for configuring a Mumble server.

        Parameters
        ----------
        slots : int
        superuser_password : str
        password : str, optional
            by default None
        motd : str, optional
            by default None

        Raises
        ------
        MultipleGames
            Raised when you attempt to create one server
            with multiple games.
        InvalidSlotSize
            Raised when slot size is below 7 or above 700.

        Returns
        -------
        ServerSettings
        """

        if self.__game:
            raise MultipleGames()

        self.__game = True

        self.payload["game"] = "mumble"

        if slots:
            if slots < 7 or slots > 700:
                raise InvalidSlotSize()

            self.payload["mumble_settings.slots"] = slots
        if superuser_password:
            self.payload["mumble_settings.superuser_password"] = \
                superuser_password
        if password:
            self.payload["mumble_settings.password"] = password
        if motd:
            self.payload["mumble_settings.welcome_text"] = motd

        return self

    def tf2(self, slots: int = None, rcon_password: str = None,
            gotv: bool = False, sourcemod: bool = False,
            insecure: bool = False, password: str = None,
            admins: list = None) -> ServerSettings:
        """Used for configuring a TF2 server.

        Parameters
        ----------
        rcon_password : str
        slots : int
        gotv : bool, optional
            by default False
        sourcemod : bool, optional
            by default False
        insecure : bool, optional
            by default False
        password : str, optional
            by default None
        admins : list, optional
            by default None

        Raises
        ------
        MultipleGames
            Raised when you attempt to create one server
            with multiple games.
        InvalidSlotSize
            Raised when slot size is below 5 or above 32.

        Returns
        -------
        ServerSettings
        """

        if self.__game:
            raise MultipleGames()

        self.__game = True

        self.payload["game"] = "teamfortress2"

        if slots:
            if slots < 5 or slots > 32:
                raise InvalidSlotSize()

            self.payload["teamfortress2_settings.slots"] = slots
        if rcon_password:
            self.payload["teamfortress2_settings.rcon"] = rcon_password
        if gotv:
            self.payload["teamfortress2_settings.enable_gotv"] = gotv
        if sourcemod:
            self.payload["teamfortress2_settings.enable_sourcemod"] = \
                sourcemod
        if insecure:
            self.payload["teamfortress2_settings.insecure"] = insecure
        if password:
            self.payload["teamfortress2_settings.password"] = password
        if admins:
            self.payload["teamfortress2_settings.sourcemod_admins"] = admins

        return self

    def valheim(self, password: str, world_name: str) -> ServerSettings:
        """Used to configure valheim server.

        Parameters
        ----------
        password : str
        world_name : str

        Returns
        -------
        ServerSettings

        Raises
        ------
        MultipleGames
        """

        if self.__game:
            raise MultipleGames()

        self.payload["game"] = "valheim"
        self.payload["valheim_settings.password"] = password
        self.payload["valheim_settings.world_name"] = world_name

        return self

    def teamspeak(self, slots: int) -> ServerSettings:
        """Used for configuring a teamspeak server.

        Parameters
        ----------
        slots : int

        Raises
        ------
        MultipleGames
            Raised when you attempt to create one server
            with multiple games.
        InvalidSlotSize
            Raised when slot size is below 5 or above 500.

        Returns
        -------
        ServerSettings
        """

        if self.__game:
            raise MultipleGames()

        self.__game = True

        if slots < 5 or slots > 500:
            raise InvalidSlotSize()

        self.payload["game"] = "teamspeak3"
        self.payload["teamspeak3_settings.slots"] = slots

        return self


class MatchSettings:
    def __init__(self, connection_time: int = 300,
                 knife_round: bool = False,
                 wait_for_spectators: bool = True,
                 warmup_time: int = 15) -> None:
        """Used to create a match.

        Parameters
        ----------
        connection_time : int, optional
            by default 300
        knife_round : bool, optional
            by default False
        wait_for_spectators : bool, optional
            by default True
        warmup_time : int, optional
            by default 15
        """

        self.payload = {
            "connection_time": connection_time,
            "enable_knife_round": knife_round,
            "wait_for_spectators": wait_for_spectators,
            "warmup_time": warmup_time
        }

    def __convert_id(self, given_id) -> str:
        """Converts any steamID format to 32.

        Parameters
        ----------
        given_id
            Given steamID.

        Returns
        -------
        str
            SteamID32

        Raises
        ------
        InvalidSteamID
            Raised when the given ID isn't understood.
        """

        if type(given_id) == int or given_id.isdigit():
            given_id = int(given_id)

            steamid = "STEAM_1:"

            steamidacct = given_id - 76561197960265728
            if steamidacct % 2 == 0:
                steamid += "0:"
            else:
                steamid += "1:"

            steamid += str(steamidacct // 2)

            return steamid

        elif "STEAM_1" in given_id or "STEAM_0" in given_id:
            return given_id.replace("STEAM_0", "STEAM_1")

        elif "[U:" in given_id:
            for ch in ["[", "]"]:
                if ch in given_id:
                    usteamid = given_id.replace(ch, "")

            usteamid_split = usteamid.split(":")

            steamid = "STEAM_1:"

            z = int(usteamid_split[2])

            if z % 2 == 0:
                steamid += "0:"
            else:
                steamid += "1:"

            steamid += str(z // 2)

            return steamid
        else:
            raise InvalidSteamID()

    def __format_players(self, players: list) -> None:
        return ",".join([self.__convert_id(steam_id) for steam_id in players])

    def playwin(self, webhook: str = None) -> MatchSettings:
        """Enables playwin AC.

        Parameters
        ----------
        webhook : str, optional
            Webhook to push playwin results, by default None

        Returns
        -------
        MatchSettings
        """

        self.payload["enable_playwin"] = True
        if webhook:
            self.payload["playwin_result_webhook_url"] = webhook

        return self

    def webhook(self, match_end: str, round_end: str,
                authorization: str = None) -> MatchSettings:
        """Used to set webhooks.

        Parameters
        ----------
        match_end : str
            URL of match end webhook.
        round_end : str
            URL of round end webhook.
        authorization : str, optional
            by default None

        Returns
        -------
        MatchSettings
        """

        self.payload["match_end_webhook_url"] = match_end
        self.payload["round_end_webhook_url"] = round_end

        if authorization:
            self.payload["webhook_authorization_header"] = authorization

        return self

    def spectators(self, players: list) -> MatchSettings:
        """Spectators

        Parameters
        ----------
        players : list
            List of spectator steam IDs,
            steamID 64, 32 & u are supported.

        Returns
        -------
        MatchSettings
        """

        self.payload["spectator_steam_ids"] = self.__format_players(players)

        return self

    def team_1(self, players: list) -> MatchSettings:
        """Team 1 players

        Parameters
        ----------
        players : list
            List of spectator steam IDs,
            steamID 64, 32 & u are supported.

        Returns
        -------
        MatchSettings
        """

        self.payload["team1_steam_ids"] = self.__format_players(players)

        return self

    def team_2(self, players: list) -> MatchSettings:
        """Team 2 players

        Parameters
        ----------
        players : list
            List of spectator steam IDs,
            steamID 64, 32 & u are supported.

        Returns
        -------
        MatchSettings
        """

        self.payload["team2_steam_ids"] = self.__format_players(players)

        return self
