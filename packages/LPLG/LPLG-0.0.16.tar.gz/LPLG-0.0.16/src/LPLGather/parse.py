__all__ = ['get_schedule_data', 'get_stage_data', 'get_match_data', 'get_team_details', 'get_player_details']

import requests
from polars import (
    col,
    collect_all, 
    Utf8, 
    UInt8, 
    UInt16, 
    UInt32,  
    Int16,
    LazyFrame, 
    Float32, 
    Boolean,
    lit
)
import logging
from logging import WARNING
import msgspec
from ._schemas._schemas import *
from ._config._config import *
from ._func._func import *
from ._func._utils import TeamDataSaver, PlayerDetailsSaver

logging.basicConfig(filename='Parse.log', level=WARNING)

def get_schedule_data() -> LazyFrame:
    """
    Fetches the schedule data from the API and returns it as a LazyFrame.
    This function sends a GET request to the API endpoint for schedule data,
    processes the JSON response, and returns the schedule data as a LazyFrame.

    Returns:
        LazyFrame: A LazyFrame containing the schedule data with columns 'seasonId'
        and 'seasonName'.

    Example:
        #   
            >>> schedule_data = get_schedule_data()
            >>> print(schedule_data)
    """
    try:

        response = requests.get(API_URL_ROOT + API_ENDPOINT_SCHEDULE, headers=API_HEADERS)
        response.raise_for_status()
        json_data = msgspec.json.decode(response.content, type=ScheduleResponse)
        data_list = [{'seasonId': str(info.seasonId), 'seasonName': info.seasonName
                      } for info in json_data.data]
        df = LazyFrame(data_list
                          ).with_columns(col('seasonId').cast(UInt32), col("seasonName"
                                                                                       ).cast(Utf8)).collect(streaming=True)
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to make the request: {e}")
        return LazyFrame({})
    except msgspec.exceptions.DecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return LazyFrame({})

def get_stage_data(seasonId: int) -> LazyFrame:
    """
    Fetches stage information for a given season ID.

    Args:
        seasonId (int): The season ID for which to fetch stage information.

    Returns:
        LazyFrame: A LazyFrame containing the stage information with columns 'stageId' and 'stageName'.

    Example:
        #
            >>> stage = get_stage_data(190)
            >>> print(stage)

    """
    try:
        seasonId_str = str(seasonId)
        response = requests.get(API_URL_ROOT + API_ENDPOINT_STAGE + "?seasonId=" + seasonId_str, headers=API_HEADERS)
        response.raise_for_status()
        json_data = msgspec.json.decode(response.text, type=StageResponse)
        stage_ids = [info.stageId for info in json_data.data.stageInfos]
        stage_names = [info.stageName for info in json_data.data.stageInfos]
        return LazyFrame({'stageId': stage_ids, 'stageName': stage_names}).filter(
                                  col("stageName") !="默认").with_columns(
                                  col('stageId').cast(UInt8), 
                                  col("stageName").cast(Utf8)).collect(streaming=True)
        
    except requests.exceptions.RequestException as e:
        return None

def get_match_data(seasonId: int, stageId: int) -> LazyFrame:
    """
    Fetches matches based on season and stage identifiers.
    This function retrieves a list of matches from a remote API based on the specified season and stage identifiers.

    Args:
        seasonId (int): The identifier of the season for which matches are to be fetched.
        stageId (int): The identifier of the stage within the season.

    Returns:
        LazyFrame: A LazyFrame containing the retrieved matches.

    Example:
        #
            >>> matches = get_match_data(190, 1)
            >>> print(matches)
    """
    seasonId_str = str(seasonId)
    stageId_str = str(stageId)
    response = requests.get(
        API_URL_ROOT + API_ENDPOINT_MATCH + "?seasonId=" + seasonId_str + "&stageId=" +
        stageId_str + "&teamId&searchTime&searchEndTime&page&size", headers=API_HEADERS)
    response.raise_for_status()
    json_data = msgspec.json.decode(response.content, type=MatchResponse)
    matches = [msgspec.structs.asdict(match) for match in json_data.data]
    return LazyFrame(matches).collect(streaming=True).with_columns(lit(seasonId).alias("seasonId"))

def get_team_details(matchid: int, seasonId: int, stageId: int) -> TeamDataSaver:
    """
    Fetches and processes team details for a given match, returning a DataSaver object
    which can be used to save the data in CSV or Parquet format.

    This function retrieves team details for a specific match using the provided match ID,
    season ID, and stage ID. It processes the data into a LazyFrame and encapsulates it within
    a DataSaver object for convenient saving in different formats.

    Args:
        matchid (int): The unique identifier of the match.
        seasonId (int): The season ID.
        stageId (int): The stage ID.

    Returns:
        An object containing the processed LazyFrame and methods for saving
        the data in CSV or Parquet format. The DataSaver object also allows
        for printing the LazyFrame to the console when the object is called in
        a print statement or evaluated in an interactive environment.

    Example:
            >>> df = get_team_details(12345, 2023, 1)
            >>> df.write_csv("team_details.csv")  
            >>> df.write_parquet("team_details.parquet")  
            >>> print(df)  
    """
    matchid = str(matchid)
    response = requests.get(API_URL_ROOT + API_ENDPOINT_DETAILS + matchid, headers=API_HEADERS)
    response.raise_for_status()
    json_data = response.json()
    json_data = msgspec.json.decode(response.content, type=DetailsResponse)
    team_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchId': matchid,
        'bo': match_info.bo,
        'teamId': team.teamId,
        'kills': team.kills,
        'baronAmount': team.baronAmount,
        'dragonAmount': team.dragonAmount,
        'turretAmount': team.turretAmount,
        'golds': team.golds,
        'banHeroList': team.banHeroList,
        'playerInfos': team.playerInfos
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    ]
    
    DF_TEAM_INFO = LazyFrame(team_list).drop('playerInfos').with_columns(
        [col("banHeroList").list.get(i).alias(
            f"ban_{i + 1}") for i in range(5)]).drop(
                "banHeroList").with_columns(
                    col('matchId').cast(UInt32), 
                    col('bo').cast(UInt8),
                    col('teamId').cast(UInt16),
                    col('kills').cast(UInt8),
                    col('baronAmount').cast(UInt8),
                    col('dragonAmount').cast(UInt8),
                    col('turretAmount').cast(UInt8),
                    col('golds').cast(UInt32),
                    col('ban_1').cast(UInt16),
                    col('ban_2').cast(UInt16),
                    col('ban_3').cast(UInt16),
                    col('ban_4').cast(UInt16),
                    col('ban_5').cast(UInt16)).collect(streaming=True)
    
    folder_path = os.path.join('Games', str(seasonId), str(stageId), str(matchid))
    os.makedirs(folder_path, exist_ok=True)
    return TeamDataSaver(DF_TEAM_INFO, folder_path)

def get_player_details(matchid: int, seasonId: int, stageId: int) -> PlayerDetailsSaver:
    """
    This function fetches player details from a game match.

    Args:
        matchid (int): The ID of the match for which you want to retrieve details.
        seasonId (int): Season ID for the match.
        stageId (int): Stage ID for the match.
        format (str): The format of the output file. Options are 'csv', 'parquet' or 'Lazyframe'. Default is 'Lazyframe'.

    Returns:
        LazyDataFrame
    """
    matchid = str(matchid)
    response = requests.get(API_URL_ROOT + API_ENDPOINT_DETAILS + matchid, headers=API_HEADERS)
    response.raise_for_status()
    json_data = response.json()
    json_data = msgspec.json.decode(response.content, type=DetailsResponse)
    PlayerInfo_list = [
        {'matchid': matchid, 'bo': match_info.bo, **msgspec.structs.asdict(Player)}
        for match_info in json_data.data.matchInfos
        for team in match_info.teamInfos
        for Player in team.playerInfos
    ]

    DF_PLAYER_INFO = (
    LazyFrame(PlayerInfo_list)
    .select([
        'matchid',
         'bo',
          'playerId',
           'playerName',
            'playerAvatar',
             col('heroId').map_dict(CHAMPION_MAP, return_dtype=Utf8).alias('ChampionName'),
             col('spell1Name').map_dict(SS_MAP, return_dtype=Utf8).alias('spell1Name'),
             col('spell2Name').map_dict(SS_MAP, return_dtype=Utf8).alias('spell2Name'),
                      'accountId',
                       'minionKilled'
                       ])
    .with_columns
    (
        col('matchid').cast(UInt32),
        col('bo').cast(UInt8),
        col('playerId').cast(UInt32),
        col('playerName').cast(Utf8),
        col('playerAvatar').cast(Utf8),
        col('spell1Name').cast(Utf8),
        col('spell2Name').cast(Utf8),
        col('accountId').cast(UInt8),
        col('minionKilled').cast(UInt16)
    )
)

    
    PlayerTrinketItem_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'trinketItem': msgspec.structs.asdict(Player.trinketItem)
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ]
    
    DF_PLAYER_TRINKET = (
        LazyFrame(PlayerTrinketItem_list
                                     ).unnest("trinketItem"
                                              ).select(
                                                  [
                                                      'seasonId',
                                                      'stageId',
                                                      'matchid',
                                                      'bo',
                                                      'PlayerId',
                                                      'PlayerName',
                                                      col('itemId').map_dict(ITEM_MAP, return_dtype=Utf8).alias('itemName')]
                                                  ).with_columns
        (
            col('matchid').cast(UInt32),
            col('bo').cast(UInt8),
            col('PlayerId').cast(UInt32),
            col('PlayerName').cast(Utf8),
            col('itemName').cast(Utf8)
        )
    )
    
    PlayerItem_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'items': msgspec.structs.asdict(item)
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    for item in Player.items
    ]
    
    DF_PLAYER_ITEM = (
        LazyFrame(PlayerItem_list)
        .unnest('items').select([
            'seasonId',
            'stageId',
            'matchid',
                'bo',
                    'PlayerId',
                        'PlayerName',
                            col('itemId').map_dict(ITEM_MAP, return_dtype=Utf8).alias('itemName')
        ])
        .with_columns(
            col('matchid').cast(UInt32),
            col('bo').cast(UInt8),
            col('PlayerId').cast(UInt32),
            col('PlayerName').cast(Utf8),
            col('itemName').cast(Utf8),
        )
    )
    
    
    PlayerperkStyle_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'perkStyle': msgspec.structs.asdict(Player.perkStyle),
        'perkSubStyle': msgspec.structs.asdict(Player.perkSubStyle)
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ] 

    DF_PLAYER_PERKS = LazyFrame(
        PlayerperkStyle_list).unnest('perkStyle').with_columns(
        perkStyle_styleId= col('styleId'),
        perkStyle_styleEn= col('styleEn')
    ).drop('styleEn').drop('styleId').unnest("perkSubStyle").with_columns(
        perkSubStyle_styleId= col('styleId'),
        perkSubStyle_styleEn= col('styleEn')).drop('styleEn').drop('styleId').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('perkStyle_styleId').cast(UInt16),
                                  col('perkStyle_styleEn').cast(Utf8),
                                  col('perkSubStyle_styleId').cast(UInt16),
                                  col('perkSubStyle_styleEn').cast(Utf8))

    PlayerperkRunes_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'perkRunes': msgspec.structs.asdict(rune),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    for rune in Player.perkRunes
    ]

    DF_PLAYER_PERKRUNES = LazyFrame(PlayerperkRunes_list).unnest('perkRunes').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('runeId').cast(UInt16),
                                  col('iconKey').cast(Utf8))
    
    PlayerbattleDetail_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'battleDetail': msgspec.structs.asdict(Player.battleDetail),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ]

    DF_PLAYER_BATTLE_DETAIL = LazyFrame(PlayerbattleDetail_list).unnest('battleDetail').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('kills').cast(UInt8),
                                  col('death').cast(UInt8),
                                  col('assist').cast(UInt8),
                                  col('kda').cast(Float32),
                                  col('highestKDA').cast(Boolean),
                                  col('highestKillStreak').cast(UInt8),
                                  col('highestMultiKill').cast(Utf8),
                                  col('attendWarRate').cast(Float32),
                                  col('highestAttendWarRate').cast(Boolean))

    PlayerdamageDetail_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'damageDetail': msgspec.structs.asdict(Player.damageDetail),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ] 
    
    DF_PLAYER_DAMEGE_DETAIL = LazyFrame(PlayerdamageDetail_list).unnest('damageDetail').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('heroDamage').cast(Float32),
                                  col('heroPhysicalDamage').cast(Float32),
                                  col('heroMagicalDamage').cast(Float32),
                                  col('heroTrueDamage').cast(Float32),
                                  col('totalDamage').cast(Float32),
                                  col('totalPhysicalDamage').cast(Float32),
                                  col('totalMagicalDamage').cast(Float32),
                                  col('totalTrueDamage').cast(Float32),
                                  col('highestCritDamage').cast(Float32),
                                  col('damageTransit').cast(Float32),
                                  col('highestDamageTransit').cast(Boolean),
                                  col('damagePerGold').cast(Float32),
                                  col('highestDamagePerGold').cast(Boolean),
                                  col('damageRate').cast(Float32),
	                              col('highestDamageRate').cast(Boolean))

    PlayerDamageTakenDetail_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'DamageTakenDetail': msgspec.structs.asdict(Player.DamageTakenDetail),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ] 
    
    DF_DEMAGE_TAKEN_DETAIL = LazyFrame(PlayerDamageTakenDetail_list).unnest('DamageTakenDetail').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('damageTaken').cast(Float32),
                                  col('physicalDamageTaken').cast(Float32),
                                  col('magicalDamageTaken').cast(Float32),
                                  col('trueDamageTaken').cast(Float32),
                                  col('takenDamageRate').cast(Float32),
                                  col('highestTakenDamageRate').cast(Boolean),
                                  col('damageTakenPerGold').cast(Float32))

    PlayerotherDetail_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'otherDetail': msgspec.structs.asdict(Player.otherDetail),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
    ] 
    
    DF_PLAYER_OTHER_DETAIL = LazyFrame(PlayerotherDetail_list).unnest('otherDetail').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('golds').cast(UInt16),
                                  col('oppositeGoldsDiff').cast(Int16),
                                  col('turretAmount').cast(UInt8),
                                  col('creepsKilled').cast(UInt16),
                                  col('level').cast(UInt8),
                                  col('firstBlood').cast(Boolean),
                                  col('firstTurret').cast(Boolean),
                                  col('firstTurretKill').cast(Boolean),
                                  col('firstTurretAssist').cast(Boolean),
                                  col('spentGold').cast(UInt16),
                                  col('totalNeutralMinKilled').cast(Float32),
                                  col('totalMinKilledYourJungle').cast(Float32),
                                  col('totalMinKilledEnemyJungle').cast(Float32))

    PlayervisionDetail_list = [
    {
        'seasonId':seasonId,
        'stageId':stageId,
        'matchid': matchid,
        'bo': match_info.bo,
        'PlayerId': Player.playerId,
        'PlayerName': Player.playerName,
        'visionDetail': msgspec.structs.asdict(Player.visionDetail),
    }
    for match_info in json_data.data.matchInfos
    for team in match_info.teamInfos
    for Player in team.playerInfos
]   
    
    DF_PLAYER_VISION_DETAIL = LazyFrame(PlayervisionDetail_list).unnest('visionDetail').with_columns(
                                  col('matchid').cast(UInt32),
                                  col('bo').cast(UInt8),
                                  col('PlayerId').cast(UInt32),
                                  col('PlayerName').cast(Utf8),
                                  col('wardPlaced').cast(UInt8),
                                  col('wardKilled').cast(UInt8),
                                  col('visionScore').cast(Float32),
                                  col('highestVisionScore').cast(Boolean),
                                  col('controlWardPurchased').cast(UInt8))
    
    DF_LIST =[DF_PLAYER_INFO,DF_PLAYER_TRINKET,DF_PLAYER_ITEM,DF_PLAYER_PERKS,DF_PLAYER_PERKRUNES,
              DF_PLAYER_BATTLE_DETAIL,DF_PLAYER_DAMEGE_DETAIL,DF_DEMAGE_TAKEN_DETAIL,DF_PLAYER_OTHER_DETAIL,DF_PLAYER_VISION_DETAIL]
    
    finals_dfs = collect_all(DF_LIST, comm_subplan_elim=False, streaming=True)
    
    folder_path = os.path.join('Games', str(seasonId), str(stageId), str(matchid))
    os.makedirs(folder_path, exist_ok=True)

    df_list = [
        ('Player_Info', finals_dfs[0]),
        ('Player_Trinket', finals_dfs[1]),
        ('Player_Item', finals_dfs[2]),
        ('Player_Perks', finals_dfs[3]),
        ('Player_Perks_Runes', finals_dfs[4]),
        ('Player_Battle_Detail', finals_dfs[5]),
        ('Player_Damage_Detail', finals_dfs[6]),
        ('Player_Damage_Taken_Detail', finals_dfs[7]),
        ('Player_Other_Detail', finals_dfs[8]),
        ('Player_Vision_Detail', finals_dfs[9]),
    ]

    return PlayerDetailsSaver(df_list, folder_path)

