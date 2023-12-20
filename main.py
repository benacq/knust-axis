import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import aiofiles
import json

from resources.ocr import extract_data
from resources.enhancer import enhance_image
from resources.search import search_student, search_student_by_reference
from resources.student_response import StudentResponse


# class for name and student number basemodel
class Student(BaseModel):
    name: str
    student_number: str


app = FastAPI()


# index route
@app.get('/')
async def root():
    return {'message': 'hello world'}


# post route for student name and student number
@app.post('/verify-student')
async def root(student: Student):
    try:
        data = search_student(student.name)
        print("RESPONSE: \n", data)

        found_student = search_student_by_reference(data, student.student_number)
        # print("\n", found_student)
        return StudentResponse.shape_response(found_student)
    except Exception as e:
        print("EXCEPTION", e)
        raise HTTPException(status_code=400, detail=str(e))


# post route to handle ocr
@app.post("/scan-id", response_class=HTMLResponse)
async def verify_id(request: Request, file: UploadFile = File(...)):
    # save image file
    async with aiofiles.open('images/image.jpg', 'wb') as f:
        content = await file.read()  # async read
        await f.write(content)  # async write

    try:
        surname, f_name, student_number = extract_data(
            enhance_image('images/image.jpg'))

        res = {
            'first_name': f_name.split(" (")[0],
            'surname': surname,
            'student_number': student_number
        }

        return JSONResponse(content=res)
    except (KeyError, AttributeError):
        raise HTTPException(
            status_code=400, detail='Could not read data from image')

        # os.remove('image/image.jpg')
        # os.remove('image/enhanced_image.jpg')


# if __name__ == '__main__':
#     uvicorn.run(app)
