# 점프 투 플라스크
> 위키독스의 점프 투 플라스크를 참고해서 만들었습니다. 우분투 환경과 맞지 않거나 현재는 

```
├── pybo/
│      ├─ __init__.py
│      ├─ models.py
│      ├─ forms.py
│      ├─ views/
│      │   └─ main_views.py
│      ├─ static/
│      │   └─ style.css
│      └─ templates/
│            └─ index.html
└── config.py
```

### __init__.py
- 해당 파일이 pybo.py 파일을 대체할 것

### models.py
- DB를 처리함
- 파이보 프로젝트는 ORM(object relational mapping)을 지원하는 파이썬 DB 도구인 SQLAlchemy를 사용
- SQLAlchemy는 모델 기반으로 DB를 처리함

### forms.py
- 웹 브라우저에서 서버로 전송된 폼을 처리할 떄 WTForms라는 라이브러리를 사용한다. 이것도 모델 기반으로 폼을 처리함

### Views 디렉터리
- 화면을 구성함
- 화면 구성 함수들로 구성된 뷰 파일들을 저장. 기능에 따라 main_view.py, qeustion_views.py 등의 뷰 파일을 만들 것

### static 디렉터리
- CSS,자바스크립트,이미지파일을 저장하는 static 디렉터리

### templates 디렉터리
- 파이보의 질문 목록, 질문 상세등의 HTML 파일 저장 

### 프로젝트를 설정하는 config.py 
- 프로젝트의 환경변수, DB등의 설정을 이 파일에 저장함


## pybo.py를 __init__으로 변경 후 FLASK_APP으로 설정

- 터미널에
``` 
export FLASK_APP=pybo:create_app 
``` 
- 하고 ``` flask run ``` 하면 __init__.py가 실행됨 

```python
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index(): pass

@app.route('/login')
def login(): pass

@app.route('/user/<username>')
def profile(username): pass

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

if __name__ == '__main__':
    app.run(debug = True)
```
- 은 이전 파일에서 만들었고, 이번에는 

```python
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_pybo():
        return 'Hello, Pybo!'

    return app
```
- 위처럼 진행된다. if 부분이 빠져있는데 왜 실행되는지 궁금해서 찾아봤다.

- Flask는 두 가지 방식으로 서버를 실행할 수 있습니다.

1. 파이썬 코드 내에서 직접 실행:
if __name__ == '__main__': app.run()
→ 이 경우, python 파일명.py로 실행합니다.

2. CLI(명령줄)에서 실행:
```flask run```
→ 이 경우, Flask가 환경 변수(FLASK_APP)로 지정한 파일에서 Flask 앱 객체를 찾아 실행합니다.

## 블루프린트로 라우팅 함수 관리하기
- 지금까지 작성한 대로라면 새로운 URL 매핑이 필요할 때마다 라우팅 함수를 create_app 함수 안에 계속 추가해야 한다. 이렇게 라우팅 함수가 계속 추가된다면 create_app 함수는 엄청나게 크고 복잡한 함수가 될 것

- create_app 함수 안에 포함된 hello_pybo 대신 블루 프린트를 사용할 수 있게 해보자
- views 디렉터리에 main_views.py 파일을 작성하자 
```python
from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello_pybo():
    return 'Hello, Pybo!'
```
- 위 어노테이션 ```@app.route```에서 ```@bp.route```로 변경되었다.
>- ` @Deprecated`역시 어노테이션의 일종이다. 어노테이션은 주로 런타임에 특정 기능을 실행시키도록 하거나 프로그램 빌드 시 코드를 자동생성 가능하도록 정보를 주는 등의 역할을 한다.


>- 데코레이터는 함수(또는 클래스)의 앞에 @데코레이터이름 형태로 붙여서, 해당 함수의 동작을 감싸거나 확장하는 역할을 합니다.
>- 동작 방식:
데코레이터는 실제로는 "함수를 인자로 받아서, 새로운 함수를 반환하는 함수"입니다.
즉, 기존 함수의 내부 코드를 수정하지 않고도, 함수의 실행 전후에 원하는 동작을 추가할 수 있습니다.

- 객체 생성시 사용된 ```__name__ ```은 모듈명인 "main_views"가 인수로 전달됨, main은 블루프린트의 별칭으로, 후에 사용할 url_for 함수에서 사용된다. 
- url_prefix에 / 대시 /main을 입력하면 localhost:5000/이 호출되는게 아닌 localhost:5000/main/이 호출된다.

- 블루 프린트 등록
- ```__init__.py```
```python
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app
```

- 블루프린트에 라우팅 함수 추가

```python
from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello/')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return 'Pybo index'
```
- 실습해본 결과 라우트에 /hello를 추가하면 404 에러 뜬다. /hello/를 추가해야 제대로 출력되니 주의하자

## 모델로 데이터 처리하기 
- pybo는 질문 답변 게시판으로 질문이나 답변을 작성하면 데이터가 생성된다. 데이터를 저장,조회,수정하는 기능을 구현해야하는데, 웹서비스는 데이터를 처리할 때 대부분 DB를 사용한다.
- DB는 SQL을 사용하는 복잡한 과정이 필요한데 ORM을 사용하면 파이썬 문법만으로 DB를 다룰 수 있음 

- 쿼리를 이용한 새 데이터 삽입 예)
```
insert into question (subject, content) values ('안녕하세요', '가입 인사드립니다 ^^');
insert into question (subject, content) values ('질문 있습니다', 'ORM이 궁금합니다');
```

- ORM을 이용한 새 데이터 삽입 예)
```python
question1 = Question(subject=’안녕하세요’, content='가입 인사드립니다 ^^')
db.session.add(question1)
question2 = Question(subject=’질문 있습니다’, content='ORM이 궁금합니다')
db.session.add(question2)
```

- ORM 라이브러리 설치 Flask-Migrate

``` pip install flask-migrate ```

- ORM을 프로젝트에 적용하렴녀 DB 설정이 필요하다. 루트에 config.py를 생성하고 

```python
# DB설정 

import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) #DB접속 주소, 설정에 의해 SQLite DB가 사용되고,DB파일은 프로젝트 홈 디렉터리 바로밑 pybo.db파일로 저장된다.
SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy의 이벤트를 처리하는 옵션, 해당 프로젝트에는 필요하지 않음
```

### ORM 적용하기 
```__init__.py```
```python
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app
```

- config파일을 읽기 위해 ```app.config.from_object(config)```를 추가, 전역 변수로 db,migrate 객체를 만든 다음 create_app함수 안에서 init_app 메서드를 이용해 app에 등록
- 플라스크는 위같은 패턴을 자주 씀, DB객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 사용할수 없기 때문에 create_app 밖에서 생성한다.
- 해당 객체를 앱에 등록할 때는 create_app 함수에서 init_app 함수를 통해 진행한다.

### DB 초기화하기
- ```flask db init```으로 DB를 초기화, 해당 명령은 최초 한 번만 수행하면 된다.
- migrations 디렉터리에 자동으로 생성한다.

#### DB 관리 명령어 정리
- 현재 프로젝트에서는 2가지의 명령어가 필요하다. 모델을 추가하거나 변경할때

|명령어|설명|
|------------------|----------------|
| ```flask db migrate```| 모델을 새로 생성하거나 변경할 때 사용 (실행시 작업 파일 생성)|
| ```flask db upgrade```| 모델의 변경 내용을 실제 DB에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 DB를 변경한다)|


## 모델 만들기
- 모델은 데이터를 다룰 목적으로 만든 파이썬 클래스

### 모델 속성 구성하기 
- 질문과 답변 모델에는 어떤 속성이 필요할까?
1. 질문 모델 속성
- id : 질문 데이터의 고유 번호
- subject : 질문 제목
- content : 질문 내용
- create_date : 질문 작성일시
2. 답변 모델 속성
- id : 답변 데이터의 고유 번호
- question_id : 질문 데이터의 고유 번호
- conetent : 답변 내용
- create_date : 답변 작성일시

#### 질문 모델 생성하기
- models.py파일에 질문 모델인 Question 클래스를 정의하여 사용할 것
```python 
from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

```
- 해당 모델 클래는 db.Model 클래스를 상속하여 만들어야 한다. 이때 만들어진 DB객체는 ```__init__.py```에서 셍상힌 SQLAlchemy 클래스의 객체

- db.Column()의 첫번째 인수는 데이터 타입 의미, 그 뒤로는
- primary_key : 기본키로 만듬
> Flask는 데이터 타입이 db.Integer이고 기본키로 설정한 속성은 값이 자동으로 증가하는 특징이 있어, 데이터를 저장할 때 값을 세팅하지 않아도 1씩 자동으로 증가되어 저장된다.
- nullable: 속성에 값을 저장할 때 빈값 허용여부

#### 답변 모델 생성
```models.py```
- 추가
```python
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
```
- Question과 Answer와 차이는 question_id와 question 밖에 없음 

- ```question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))``` : question_id 속성은 답변을 질문과 연결하기 위해 추가한 속성, 답변은 어떤 질문에 대한 답변이지 알아야 하므로 질문 ID의 속성이 필요하다. 그래서 db.ForeignKey가 필요한 것.
- db.ForeignKey의 첫 파라미터 question_id는 퀘스천 테이블의 id 컬럼과 연결된다는 뜻, 해당 모델을 통해 테이블 생성시 테이블명은 question이다.
- 두 번째 파라미터 ondelete는 삭제 연동 설정이다. 즉, ```ondelete='CASCADE'```는 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다는 의미, CASCADE 옵션은 DB설정이다. 따라서 질문을 DB 툴에서 쿼리로 삭제할 때만 질문에 달린 답변들이 삭제된다.

- ```question = db.relationship('Question', backref=db.backref('answer_set'))``` : 해당 속석은 답변 모델에서 질문 모델을 참조하기 위해 추가됨, db.relationship으로 question 속성을 생성하면 답변 모델에서 연결된 질문 모델의 제목을 answer.question.subject 처럼 참조할 수 있다.
- 첫 번째 파라미터는 참조할 모델명이고 두 번째 backref 파라미터는 역 참조 설정이다. 역참조란 질문에서 답변을 거꾸로 참조한다는 의미, 

> 파이썬 코드를 이용해 질문 데이터 삭제시 연관된 답변데이터를 모두 삭제하는 방법: 파이썬 코드로 질문 데이터 삭제시, 질문과 연결된 답변 데이터는 삭제 안되고 question_id 컬럼만 빈 값으로 업데이트 된다. 파이썬 코드로 질문 데이터 삭제시 db.backref 설정에 cascade='all, delete-orphan'를 추가해야 한다. ```question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))```


## 모델 이용해 테이블 자동으로 생성하기
### 모델 import

```python
# ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
```
- 해당 코드를 ```__init__.py```의 create app에 추가한다.
### 리비전 파일 생성
- 후 터미널에 ```flask db migrate``` 입력 
- migrations 디렉토리의 version 디렉토리에 DB 변경 작업을 위한 리비전 파일이 생성된다.

### 리비전 파일 실행하기 
```flask db upgrade```
- 홈디렉터리에 pybo.db 파일이 생성
- db 파일을 열기 위해선 SQLite 필요
- https://sqlitebrowser.org/dl/

#### SQLite 우분투 설치방법
```
sudo add-apt-repository -y ppa:linuxgndu/sqlitebrowser-testing
```
```
sudo apt-get update
```
```
sudo apt-get install sqlitebrowser
```
- 그 파일 탐색기에서 디렉토리에서 db파일 실행시, 테이블 목록을 보면 question, answer 테이블이 생성되었음을 확인할 수 있다.


### 모델 사용하기
### 플라스크 셸 실행하기
```flask shell```
- 쉘 스크립트가 시작된다.

#### 질문 저장하기
```
>>> from pybo.models import Question, Answer
>>> from datetime import datetime
>>> q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())
```
- 변수 q를 만들었다고 DB에 질문 데이터가 저장되는 것은 아님 아래처럼 db 변수를 이용해야함.

```
>>> from pybo import db
>>> db.session.add(q)
>>> db.session.commit()
```
- db.session은 데이터베이스와 연결된 세션, 즉 접속된 상태를 의미
- 신규 데이터를 저장할 때는 db.session의 add 함수를 사용한 다음 commit 함수까지 실행해야함. 

- 제대로 생성되었는지 확인하려면 ```q.id``` 1 출력시 잘된거
- 작업을 취소하고 싶다면 ```db.session.rollback()```으로 되돌리기를 실행하면 됨


#### 데이터 조회하기
- DB에 저장된 데이터 조회
```Question.query.all()```
- [<Question 1>, <Question 2>] 출력됨

- filtter 함수를 이용해 첫 번째 질문 조회 가능 ```Question.query.filter(Question.id==1).all()```
- get을 이용한 조회도 가능 ```Question.query.get(1)```
- get 함수의 리턴은 단 1건만 가능

- filter와 like를 조합해 제목에 "플라스크"라는 문자열이 포함된 질문 조회 가능
```Question.query.filter(Question.subject.like('%플라스크%')).all()```

- 플라스크%: "플라스크"로 시작하는 문자열
- %플라스크: "플라스크"로 끝나는 문자열
- %플라스크%: "플라스크"를 포함하는 문자열

#### 데이터 수정하기
- 단순 대입 연산자를 사용하면 됨
```
>>> q = Question.query.get(2)
>>> q 
>>> q.subject = 'Flask Model Question'
>>> db.session.commit()
```
- 커밋해야 DB에 반영됨

#### 데이터 삭제하기
```
>>> q = Question.query.get(1)
>>> db.session.delete(q)
>>> db.session.commit()
```
- 조회하면 질문이 사라진것을 볼 수 있음

#### 답변 데이터 저장
```
>>> from datetime import datetime
>>> from pybo.models import Question, Answer
>>> from pybo import db
>>> q = Question.query.get(2)
>>> a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=datetime.now())
>>> db.session.add(a)
>>> db.session.commit()
>>> a.id
1
>>> a = Answer.query.get(1)
>>> a
<Answer 1>
```

#### 답변에 연결된 질문 찾기 vs 질문에 달린 답변 찾기
```
>>> a.question
<Question 2>
```
- 연결된 질문 찾기 Answer 모델에 question 속성이 정의되어 있음
- Answer 모델의 question 속성에 역참조 설정 ```backref=db.backref('answer_set')```이 적용되어 있음
```
>>> q.answer_set
[<Answer 1>]
```

## 질문 목록 만들기
- 메인에서 게시판 질문 목록이 출력되도록 main_views.py 파일 수정, index 함수가 문자열을 반환하던 부분을 질문 목록을 출력하도록 변경
```python
from flask import Blueprint, render_template
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello/')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

```
- 질문 목록 데이터는 ```question_list = Question.query.order_by(Question.create_date.desc())```
- 작성일시 순으로 조회하려면 ```question_list = Question.query.order_by(Question.create_date)```로 조회하면 된다. 오름차순 내림차순
- render_template 함수는 템플릿 파일을 화면으로 렌더링 하는 함수이다. 조회한 질문 목록 데이터를 render_template 함수의 파라미터로 전달하면 템플릿에서 해당 데이터로 화면을 구성한다.

### 질문 목록 템플릿 작성하기
- render_template함수에서 사용할 템플릿 파일 작성해야함
- pybo/templates/question/question_list.html 경로로 파일 작성

```html
<!-- 질문 목록 -->
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="/detail/{{ question.id }}/">{{ question.subject }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>질문이 없습니다.</p>
{% endif %}
```
- {% 와 %}로 둘러싸인 문장은 템플릿 태그, 해당 태그가 파이썬 코드와 연결됨, 살펴보면 맨 첫줄 if 부분은 render_template 함수에서 전달받은 질문 목록 데이터 question_list가 존재하는지 확인
- ```{% for question in question_list %}``` : question_list에 저장된 데이터를 하나씩 꺼내 question 객체에 대입
- ```{{ question.id }}``` 은 객체의 id를 출력함 

### 플라스크에서 자주 사용되는 템플릿태그 3가지
1. 분기문 태그 :파이썬의 if, elif, else 문과 유사하게 사용 됨
```html
{% if 조건문1 %}
    <p>조건문1에 해당하면 실행</p>
{% elif 조건문2 %}
    <p>조건문2에 해당하면 실행</p>
{% else %}
    <p>조건문1, 2 모두 해당하지 않으면 실행</p>
{% endif %}
```

2. 반복문 태그
```html
{% for item in list %}
    <p>순서: {{ loop.index }} </p>
    <p>{{ item }}</p>
{% endfor %}
```

|loop 객체의 속성|	설명|
|----------------|------------|
|loop.index	|반복 순서, 1부터 1씩 증가|
|loop.index0 |반복 순서, 0부터 1씩 증가|
|loop.first	|반복 순서가 첫 번째 순서이면 True 아니면 False|
|loop.last	|반복 순서가 마지막 순서이면 True 아니면 False|

3. 객체 태그
```{{객체.속성}}```
- 위처럼 객체의 속성은 점으로 이어서 출력가능

### 질문 상세 기능 만들기
- flask run 하면 보이는 질문의 링크로 진입하면 404 뜬다 왜? url을 보면 http://localhost:5000/detail/2/ 라고 나와있는데, 우리는 해당 url을 정의하지 않았다.

#### 라우팅 함수 
- 이것도 main_views.py를 고치면 된다.
```python
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question)
```

- detail 함수의 매개변수 question_id에는 URL 매핑 규칙에 사용한 ```<int:question_id>```가 전달됨
- ```http://localhost:5000/detail/[[MARK]]2[[/MARK]]/``` 페이지를 요청하면 main_views.py 파일의 detail 함수가 실행되고, 매개변수 question_id에는 2라는 값이 전달된다.
- URL 매핑 규칙에 있는 int는 question_id에 숫자값이 매핑됨을 의미한다.

#### 질문 상세 템플릿 작성하기
```question/question_detail.html```
```html
<h1>{{ question.subject }}</h1>
<div>
    {{ question.content }}
</div>
```

- {{ question.subject }}와 {{ question.content }}의 question은 render_template 함수에 전달한 질문 객체이다.

##### 404 에러 출력하기 
- 원래는 그냥 빈 공간이 나오지만 404 Error를 출력할 수 있다.
- main_views를 고치면 된다.
```html
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)
```
- 이 부분에서 ```query.get_or_404```로 고쳐주면  404 에러가 출력된다.

### 블루 프린트로 기능 분리하기
- 지금까지 계속 view_main에 구현했지만 블루프린트로 파일을 분리한다면 유지,보수 하는데 유리하다
#### 질문 목록, 질문 상세 기능 분리하기
- question_views.py 파일을 새로 만들고 질문 목록과 질문 상세 기능을 이동해 보자.
```python
from flask import Blueprint, render_template

from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question) 
```
- main_views.py 파일의 내용을 그대로 복사하되, 블루프린트 객체를 생성할 때 question이라는 별칭을 사용하고, url_prefix에는 /question을 사용해 main_views.py 파일의 블루프린트와 구별, ndex 함수명을 _list로 바꾸고 URL 매핑 규칙도 /에서 /list/로 바꿨다.

- ```pybo/__init__.py``` 파일도 수정하자.
```python
def create_app():
    (...생략...)

    # 블루프린트
    from .views import main_views, question_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
```

#### url_for로 리다이렉트 기능 추가
```main_views.py```
```python
from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('question._list'))
```
- detail 함수 제거하고 index함수가 question_list에 해당하는 URL로 리다이렉트하도록 코드를 수정
- redirect(URL) : URL로 페이지 이동
- url_for(라우팅 함수명) : 라우팅 함수에 매핑되어 있는 URL을 리턴, 라우팅 함수명은 'question','_list' 순서로 해석되어 라우팅 함수를 찾음
    - question은 등록된 블루프린트 별칭, _list는 블루프린트에 등록된 함수명임, questio_views파일의 _list 함수를 의미 
    - 그리고 url_for('question_list')은 /question/listURL을 반환한다.


#### 하드 코딩된 URL에 url_for 함수 이용하기
- /question_list.html 은 상세페이지로 연결하는 링크가 /detail/{{ question.id }}/ 처럼 하드 코딩되어 있다.

```html
<!-- 질문 목록 -->
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="{{ url_for('question.detail', question_id=question.id) }}">{{ question.subject }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>질문이 없습니다.</p>
{% endif %}
```
- 해당 부분을 url_for를 이용해 바꾸면 