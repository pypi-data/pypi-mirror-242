from source.request.req import *
import json
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class Group:
    def __init__(self, groupID, rbxCookie=None, isProxy=False, proxy=None, timeout=10):
        self.groupID = groupID
        self.cookie = rbxCookie
        self.isProxy = isProxy
        self.proxy = proxy
        self.timeout = timeout
        self.groupInfo = self.getGroupInfo()
        self.groupAssets = self.getGroupAssets()

    def getGroupInfo(self):
        r = Request(isProxy=self.isProxy, proxy=self.proxy, timeout=self.timeout)
        url = f"https://groups.roblox.com/v1/groups/{self.groupID}"
        response = r.getRequest(url)
        data = response.json()
        r.shutdown()

        if 'errors' in data:
            print(data['errors'][0]['userFacingMessage'])
            return None

        ownerData = data.get("owner")
        if ownerData:
            owner = {
                "groupOwnerID": ownerData.get("userId", ""),
                "groupOwnerUser": ownerData.get("username", ""),
                "groupOwnerDisplay": ownerData.get("displayName", ""),
                "groupOwnerVerified": ownerData.get("hasVerifiedBadge", ""),
            }
        else:
            owner = None

        shoutData = data.get("shout")
        if shoutData:
            shout = {
                "shoutBody": shoutData.get("body", ""),
                "shoutCreator": shoutData.get("poster", {}),
                "shoutCreated": shoutData.get("created", ""),
                "shoutUpdated": shoutData.get("updated", "")
            }
        else:
            shout = None

        groupInfo = {
            "groupInfo": {
                "groupID": data.get("id", ""),
                "groupName": data.get("name", ""),
                "memberCount": data.get("memberCount", 0),
                "groupDescription": data.get("description", ""),
                "hasVerifiedBadge": data.get("hasVerifiedBadge", False),
                "isClaimable": not owner and not data.get("isBuildersClubOnly", False) and data.get("publicEntryAllowed", False),
                "groupShout": shout
            },
            "groupOwnerInfo": owner,
            "groupPermissions": {
                "isBuildersClubOnly": data.get("isBuildersClubOnly", False),
                "publicEntryAllowed": data.get("publicEntryAllowed", False)
            }
        }
        return groupInfo

    def getGroupAssets(self):
        r = Request(isProxy=self.isProxy, proxy=self.proxy, timeout=self.timeout)

        def getFunds():
            if not self.cookie:
                return "needs-auth"
            try:
                headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
                url = f"https://economy.roblox.com/v1/groups/{self.groupID}/currency"
                req = r.getRequest(url, headers=headers)
                data = req.json()
                return data.get("robux")
            except Exception as e:
                print(e)
                return "error"

        def getPFunds():
            if not self.cookie:
                return "needs-auth"
            try:
                headers = {'Cookie': f".ROBLOSECURITY={self.cookie}"}
                today = datetime.now().strftime("%Y-%m-%d")
                url = f"https://economy.roblox.com/v1/groups/{self.groupID}/revenue/summary/{today}"
                req = r.getRequest(url, headers=headers)
                data = req.json()
                return data.get("pendingRobux")
            except Exception as e:
                return "error"

        def getClothing():
            try:
                url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={self.groupID}&ResultsPerPage=100&CreatorType=2"
                req = r.getRequest(url)
                data = req.json()
                clothes = data.get("data", [])
                groupClothing = len(clothes)

                while True:
                    if c := data.get("nextPageCursor"):
                        url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={self.groupID}&ResultsPerPage=100&CreatorType=2&cursor={c}"
                        req = r.getRequest(url)
                        data = req.json()
                        clothes = data.get("data", [])
                        groupClothing += len(clothes)
                    else:
                        break

                return groupClothing
            except Exception as e:
                return "error"

        def getGames():
            try:
                url = f"https://games.roblox.com/v2/groups/{self.groupID}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc"
                req = r.getRequest(url)
                data = req.json()
                games = data.get("data", [])
                groupVisits = sum(game.get("placeVisits", 0) for game in games)
                groupGames = len(games)
                return groupGames, groupVisits
            except Exception as e:
                return "error", "error"

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda f: f(), [getFunds, getPFunds, getClothing, getGames]))

        funds, pFunds, clothing, (games, visits) = results

        funds, pFunds, clothing, (games, visits) = results

        return {
            "groupAssets": {
                "groupFunds": funds,
                "groupPendingFunds": pFunds,
                "groupClothing": clothing,
                "groupGames": games,
                "groupGameVisits": visits
            }
        }

    def getGroupAll(self):
        groupInfo = self.getGroupInfo()
        groupAssets = self.getGroupAssets()

        return {
            **groupInfo,
            **groupAssets
        }
