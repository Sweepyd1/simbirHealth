from loader import protected


@protected.get("/History/account/{id}")
async def get_account_history(id):
    pass


@protected.get("/History/{id}")
async def get_history(id):
    pass

@protected.post("/History")
async def post_history(id):
    pass


@protected.put("/History/{id}")
async def put_history(id):
    pass





