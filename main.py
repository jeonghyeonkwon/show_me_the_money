from fastapi import FastAPI, Depends, HTTPException, status, Request
import uvicorn, dotenv, os, argparse

from setting import settings
from util.util import UtilService
from router.naver import router as naver_router
from router.upbit import router as upbit_router
from router.candle import router as candle_router
from router.candle_test import router as candle_test_router
from dtos.user_response import UserResponse
from dtos.user_request import LogInRequest, ReqAccessDto
from models.user import User, UserAccessLog
from models.enum import ReqResult
from repository.user_repository import UserRepository


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

parse = argparse.ArgumentParser()
parse.add_argument("-active", default=os.environ["active"])

args = parse.parse_args()

app = FastAPI()


@app.get("/init")
def init_user(
    utilService: UtilService = Depends(), userRepo: UserRepository = Depends()
):
    is_user: str | None = userRepo.is_exists_user(settings.init_user)
    if not is_user:
        dtos: UserResponse = utilService.init_user()
        user: User = User.create(dtos)
        savedUser: User = userRepo.create(user)
        return savedUser.userId
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 만들어짐")


@app.post("/sign-in")
def sign_in(
    request: Request,
    req: LogInRequest,
    userRepo: UserRepository = Depends(),
    utilSerivce: UtilService = Depends(),
):
    access_dto: ReqAccessDto = ReqAccessDto(request)
    find_user: User | None = userRepo.findByUserId(req.userId)

    if not find_user:
        # 아이디 체
        access_log: UserAccessLog = UserAccessLog.create(ReqResult.아이디_없음, access_dto)
        userRepo.insertLog(access_log)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디 없음")

    else:
        verify_user: bool = utilSerivce.verify_password(req.userPwd, find_user.password)
        if not verify_user:
            # 비밀번호 체크
            access_log: UserAccessLog = UserAccessLog.create(
                ReqResult.비밀번호_틀림, access_dto
            )

            userRepo.insertLog(access_log)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호 틀림"
            )
        else:
            # 토큰 발행
            return utilSerivce.create_jwt(find_user.userId)


def main():
    if args.active == "prod":
        uvicorn.run("main:app", host="127.0.0.1", port=8000)
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    directory = ["./graph/candle"]
    print(os.path)

    for p in directory:
        if not os.path.exists(p):
            os.makedirs(p)

    main()


app.include_router(naver_router, prefix="/naver")
app.include_router(upbit_router, prefix="/upbit")
app.include_router(candle_router, prefix="/candle")
app.include_router(candle_test_router, prefix="/candle-test")
