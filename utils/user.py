# from utils.mongo import MongoDB


# class UserProfile:
#     def __init__(self, _id):
#         self.id = _id
#         self.db = MongoDB("Profiles")

#     async def add_pred(self, match, score1, score2):
#         await self.db.add_or_update(self.id, {"predictions": {match: f"{score1}-{score2}"}})

#     async def add_pred_result(self, match, correct_score1, correct_score2):
#         all_pred = await self.get_all_pred()
#         score1, score2 = all_pred[match]
#         if score1 == correct_score1 and score2 == correct_score2:
#             result = "Correct"
#         elif score1 - score2 == correct_score1 - correct_score2:
#             result = "Correct Goal Difference"
#         else:
#             result = "Wrong prediction"
#         await self.db.add_or_update(self.id, {"predictions": {match: f"{score1}-{score2}  ({result})"}})
        
#     async def get_all_pred(self):
#         profile = await self.db.find_by_id_async(self.id)
#         return profile["predictions"]
