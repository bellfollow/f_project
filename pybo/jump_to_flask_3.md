# 점프 투 플라스크
> 위키독스의 점프 투 플라스크를 참고해서 만들었습니다. 우분투 환경과 맞지 않거나 현재는 다른 부분을 조금 수정했습니다. 
> 3-04부터 시작합니다.

```
pybo/
├── __init__.py           # Flask 애플리케이션 초기화 파일
├── config.py            # 애플리케이션 설정 파일
├── filter.py           # Jinja2 템플릿 필터 정의
├── forms.py            # 웹 폼 정의 (WTForms)
├── models.py           # 데이터베이스 모델 정의
├── migrations/         # 데이터베이스 마이그레이션 파일들
├── static/            # 정적 파일 (CSS, JavaScript, 이미지 등)
├── templates/         # HTML 템플릿 파일들
│   ├── auth/         # 인증 관련 템플릿
│   ├── base.html     # 기본 템플릿 (레이아웃)
│   ├── form_errors.html  # 폼 에러 메시지 템플릿
│   ├── navbar.html   # 네비게이션 바 템플릿
│   └── question/     # 질문 관련 템플릿
└── views/            # 뷰 함수들 (루트, 질문, 답변 등)
```

### __init__.py
- 해당 파일이 pybo.py 파일을 대체할 것
- Flask 애플리케이션의 초기화 및 블루프린트 설정

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
    - base.html: 모든 페이지의 기본 레이아웃
    - navbar.html: 네비게이션 바
    - auth/: 로그인/회원가입 관련 템플릿
    - question/: 질문 관련 템플릿
### 프로젝트를 설정하는 config.py 
- 프로젝트의 환경변수, DB등의 설정을 이 파일에 저장함



#### 실행하기
``` export FLASK_APP=pybo:create_app ``` 
- pybo 밖에서 터미널로 해당 명령어 실행
``` flask run ```
- flask 시작

#### DB migrate
- flask db migrate 명령으로 리비전 생성
- init이 없다는 에러메세지가 가끔 뜨는데 

```shell
flask db revision --rev-id 'migrate 안 .py의 숫자부분 입력'
flask db migrate
flask db upgrade
```

## 게시물에 일련번호 추가하기
### 게시물 번호 문제
- 페이지를 이동해도 번호가 1~10까지만 나오는것을 알 수 있다.
### 게시물 번호 공식 만들기
- ex)게시물이 12개 -> 12개~3번째 게시물이, 2페이지에는 2~1번째 게시물이 역순으로 표시되어야 함
> 번호 = 전체 게시물 개수 - (현재 페이지 -1)*페이지당 게시물 개수 - 나열 인덱스

|항목|	설명|
|--------|------------|
|번호|	최종 표시될 게시물 번호|
|전체 게시물 개수|	데이터베이스에 저장된 게시물 전체 개수|
|현재 페이지|	페이징에서 현재 선택한 페이지|
|페이지당 게시물 개수|	한 페이지당 보여줄 게시물의 개수|
|나열 인덱스|	for 문 안의 게시물 순서|

### 게시물 번호 공식을 질문 목록 템플릿에 적용하기
```question_list.html```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <table class="table">
        (... 생략 ...)
        <tr>
            <td>{{ question_list.total - ((question_list.page-1) * question_list.per_page) - loop.index0 }}</td>
            <td>
                <a href="{{ url_for('question.detail', question_id=question.id) }}">{{ question.subject }}</a>
            </td>
            <td>{{ question.create_date|datetime }}</td>
        </tr>
        (... 생략 ...)
    </table>
    (... 생략 ...)
</div>
{% endblock %}

```

|항목|	설명|
|---------|-----------|
|question_list.total	|전체 게시물 개수|
|question_list.page	|현재 페이지|
|question_list.per_page|	페이지당 게시물 개수|
|loop.index0	|나열 인덱스(0부터 시작)|

### 질문에 달린 답변 개수 표시하기
```question_list.html```

```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <table class="table">
        (... 생략 ...)
        <tr>
            <td>{{ question_list.total - ((question_list.page-1) * question_list.per_page) - loop.index0 }}</td>
            <td>
                <a href="{{ url_for('question.detail', question_id=question.id) }}">{{ question.subject }}</a>
                {% if question.answer_set|length > 0 %}
                <span class="text-danger small mx-2">{{ question.answer_set|length }}</span>
                {% endif %}
            </td>
            <td>{{ question.create_date|datetime }}</td>
        </tr>
        (... 생략 ...)
    </table>
    (... 생략 ...)
</div>
{% endblock %}
```
- {% if question.answer_set|length > 0 %}로 답변이 있는 경우를 검사하고, {{ question.answer_set|length }}로 답변 개수를 표시
- 질문 오른쪽에 빨간색 숫자가 표시, 개인적으로 대괄호 안에 해당 결과물이 나왔으면 해서 약간 코드 수정했다. 어려운거 아니다.
```html
                <span class="text-danger small mx-2">[{{ question.answer_set|length }}]</span>

```
- 대괄호 추가만 해주면 된다.

## 회원 가입
- 웹 사이트의 핵심 기술

### 회원 모델
- 다음과 같은 속성이 필요함
|속성|	설명|
|--------|-----------|
|username	|사용자 이름(ID)|
|password	|비밀번호|
|email	|이메일|

- model.py를 열어 정의한 속성 User 모델 작성
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
```
- id는 자동으로 증가하는 User 모델의 기본 키
- username, password, email에는 null값을 허용하지 않도록 nullable=False로 설정
- sername, email에는 unique=True를 지정하여 두 값이 중복되어 저장되지 않도록 함

- flask db migrate 명령으로 리비전 생성
- init이 없다는 에러메세지가 가끔 뜨는데 

```shell
flask db revision --rev-id 'migrate 안 .py의 숫자부분 입력'
flask db migrate
flask db upgrade
```
- 해당 과정을 진행해보자.

### 회원가입 폼
- form.py에 UserCreateForm을 만들자
```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

(... 생략 ...)

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

```
- 클래스명 UserCreateForm이다. username은 필수항목이고, 길이가 3-25 사이여야 한다는 검증조건을 설정함
- Length는 폼 유효성 검증시 문자열의 길이가 최소길이(min)와 최대길이(max) 사이에 해당하는지를 검증함
- password1과 password2는 "비밀번호"와 "비밀번호확인"에 대한 필드, 로그인시 하나만 필요하지만, 계정생성에선 비밀번호 맞는지 확인해야하니 2개
- password1과 password2 속성은 PasswordField로 생성되었다. StringField와 비슷하지만 템플릿에서 자동변환으로 사용시 ```<input type="password">``` 태그로 변환되는 차이점이 있음, 
- 패스워드 두개의 값이 일치해야 하는 EqualTo 검증도 추가, 속성에 지정된 ```EqualTo('password2')``` 는 password1과 password2의 값이 일치해야 함을 의미

-  EmailField로 생성되었다. EmailField 역시 StringField와 동일하지만 템플릿 자동변환으로 사용시 <input type="email"> 태그로 변환됨
- email 속성에는 필수값 검증조건에 더하여 Email() 검증조건이 추가되었다. Email() 검증조건은 해당 속성의 값이 이메일형식과 일치하는지를 검증함
- Email() 검증을 사용하기 위해서는 다음처럼 email-validator를 설치해야 한다.
```shell
pip install email_validator
```
## 회원가입 구현하기
- 회원가입을 위한 블루프린트 만들어 보기, 회원가입은 main_view.py,question_views.py,answer_views.py 어디에도 해당되지 않으므로 따로 만들어야함
```auth_views.py```

```python
from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)
```
- /auth/로 시작하는 URL이 호출되면 auth_views.py 파일의 함수들이 호출될 수 있도록 블루프린트 객체 bp를 생성함
- 회원가입을 위한 signup 함수를 생성했다. signup 함수는 POST 방식에는 계정을 저장하고 GET 방식에는 계정 등록 화면을 출력
- 계정 등록시 username으로 데이터를 조회해 이미 등록된 사용자인지 확인함
- flash는 필드 자체 오류가 아닌 프로그램 논리 오류를 발생시키는 함수
- 비밀번호는 폼으로 전달받은 값을 저장하지 않고 generate_password_hash 함수로 암호화하여 저장함
- generate_password_hash 함수로 암호화한 데이터는 복호화할 수 없음, 로그인할 때 입력받은 비밀번호는 암호화하여 저장된 비밀번호와 비교해야함

### 블루 프린트 등록
- init 함수에 등록해야함

```python
(... 생략 ...)

def create_app():
    (... 생략 ...)

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    (... 생략 ...)

    return app

```

### 회원가입 템플릿
- signup.html 파일은 템플릿 디렉토리 아래에 auth 디렉터리를 추가한 파일작성
```html
{% extends "base.html" %}
{% block content %}
<div class="container">
    <h5 class="my-3 border-bottom pb-2">계정생성</h5>
    <form method="post">
        {{ form.csrf_token }}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" name="username" id="username"
                   value="{{ form.username.data or '' }}">
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" name="password1" id="password1"
                   value="{{ form.password1.data or '' }}">
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" name="password2" id="password2"
                   value="{{ form.password2.data or '' }}">
        </div>
        <div class="mb-3">
            <label for="email">이메일</label>
            <input type="text" class="form-control" name="email" id="email"
                   value="{{ form.email.data or '' }}">
        </div>
        <button type="submit" class="btn btn-primary">생성하기</button>
    </form>
</div>
{% endblock %}
```

- 회원가입을 위한 "사용자 이름", "비밀번호", "비밀번호 확인", "이메일"에 해당되는 input 엘리먼트를 추가
- <생성하기> 버튼을 누르면 폼 데이터가 POST 방식으로 /auth/signup/ URL로 요청됨
- 회원가입을 할 때 발생할 수 있는 오류를 표시하도록 {% include "form_errors.html" %}를 사용함


### 오류 표시하기
- form_error.html 템플릿 파일은 다음과 같이 "필드에서 발생한 오류를 표시하는 부분"과"flash를 거치면서 발생한 오류를 표시하는 부분" 으로 구성됨
- 필드오류는 폼 vaildators 검증에 실패한 경우 표시되고, flash 오류는 이미 존재하는 사용자 입니다와 같은 로직에 의해 표시된다.

### 회원가입 링크
- 회원가입으로 이동할 수 있는 링크를 네비게이션 바에 추가
```navbar.html```
```html
<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Pybo</a>
        (... 생략 ...)
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('auth.signup') }}">계정생성</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```
- nav-link중 게정 생성에 해당 하는 부분의 href부분을 채우면 된다.

### 회원 데이터 확인
```shell
flask shell
Python 3.12.7 (main, Feb  4 2025, 14:46:03) [GCC 14.2.0] on linux
App: pybo
Instance: /mnt/workspace/f_project/instance
>>> from pybo.models import User
>>> User.query.all()
[<User 1>]
>>> User.query.first().username
'monkey'
```

## 로그인과 로그아웃
## 로그인
### 로그인 폼
- UserLoginForm 만들기
```form.py```
```python
(... 생략 ...)

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

```

- username, password 필드를 추가하고 각각 필수 입력 항목으로 지정하고, username의 길이는 3~25자로 제한

### 로그인 라우팅 함수
```auth_views.py```
```python
from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm

(... 생략 ...)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

```

- Login 함수는 signup 함수와 비슷하게 동작함, POST 방식에는 로그인을 수행하고, GET 요청에는 로그인 화면을 보여줌
- POST 요청에 의해 로그인 하는 과정, 폼 입력 받은 유저네임으로 DB에 해당 사용자가 있는지 검사함. 사용자 없으면 존재하지 않는 사용자 입니다 라는 오류 발생시킴, 사용자가 존재한다면 폼 입력으로 받은 password와 chech_password_hash 함수를 사용하여 DB의 비밀번호와 일치하는지를 비교함
> 이전에 복호화는 안된다 했으니 해당 패스워드를 비교하기 위해선 비밀번호를 암호화해서 비교해야한다. 
- 사용자도 존재하고, 비밀번호도 일치하면 플라스크 Session에 사용자 정보를 저장한다. 세션 키에 user_id라는 문자열을 저장하고 키에 해당하는 값은 DB에서 조회한 사용자의 id값을 저장했다.
- 세션은 request와 마찬가지로 플라스크가 자체적으로 생성하여 제공하는 객체다. 브라우저가 플라스크 서버에 요청을 보내면 request 객체는 요청할 때마다 새로운 객체가 생성된다. seeison은 request와 달리 한번 생성하면 그 값을 계속 유지하는 특징이 있다.
> 세션은 서버에서 브라우저별로 생성되는 메모리 공간이라 볼 수 있음
- 세션에 사용자의 ID 값을 저장하면 다양한 URL 요청에 이 세션에 저장된 값을 읽을 수 있다.

> 쿠키와 세션 이해하기
> 웹프로그램은 [웹 브라우저 요청 -> 서버 응답] 순서로 실행되며, 서버 응답이 완료되면 웹 브라우저와 서버 사이의 네트워크 연결은 끊어진다. 수 많은 브라우저가 서버에 요청할 때 마다 세션을 만드는게 아닌 동일한 브라우저의 요청은 동일한 세션을 사용한다.
> 서버는 어떻게 세션을 맺을까? 쿠키로 맺는다. 쿠키는 서버가 웹 브라우저에 발행하는 값으로 웹 브라우저가 서버에 어떤 요청을 하면 서버는 쿠키를 생성하여 전송하는 방식으로 응답한다. 웹 브라우저는 서버에서 받은 쿠키를 저장하고 서버에 요청을 다시 보내면 저장한 쿠키를 HTTP 헤더에 담아서 전송한다. 서버는 웹 브라우저가 보낸 쿠키를 이전에 발행했던 쿠키값과 비교해 같은 웹 브라우저에서 보낸 요청인지 구별할 수 있다. 이 때 세션은 쿠키 1개당 생성되는 서버의 메모리 공간이라고 할 수 있다.

### 로그인 템플릿
```auth/login.html```
```html
{% extends "base.html" %}
{% block content %}
<div class="container">
    <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <form method="post">
        {{ form.csrf_token }}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" name="username" id="username"
                   value="{{ form.username.data or '' }}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" name="password" id="password"
                   value="{{ form.password.data or '' }}">
        </div>
        <button type="submit" class="btn btn-primary">로그인</button>
    </form>
</div>
{% endblock %}
```
- 그인 폼에서 생성한 필드 2개(username, password)를 input 엘리먼트로 만듬
- 템플릿에서 로그인 버튼을 누르면 form 엘리먼트가 POST 방식으로 현재 웹 브라우저의 주소 창에 표시된 URL인 /auth/login/로 요청될 것


### 로그인 링크
- 네비게이션 바에 로그인 링크를 추가
```navbar.html```
```html
<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Pybo</a>
        (... 생략 ...)
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            (... 생략 ...)
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('auth.signup') }}">계정생성</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('auth.login') }}">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### 로그아웃
- 로그인을 성공해도 로그인 링크가 남아있다. 이 링크는 "로그아웃" 링크로 바뀌어야 한다. 반대도 당연하다
- 로그인 여부는 session에 저장된 값을 조사하면 알 수 있다. 

#### 로그인 여부 확인
- 로그인한 사용자 정보를 조회하여 사용할 수 있도록 auth_view.py 파일에 load_logged_in_user 함수를 다음처럼 구현해보자.
```python
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

(... 생략 ...)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
```
- ```@bp.before_app_request``` 어노테이션을 사용했다. 이 애너테이션이 적용된 함수는 라우팅 함수보다 항상 먼저 실행된다. 앞으로 load_logged_in_user 함수는 모든 라우팅 함수보다 먼저 실행될 것이다. 
> @bp.before_app_request를 적용한 함수는 auth_views.py의 라우팅 함수 뿐만 아니라 모든 라우팅 함수보다 항상 먼저 실행된다.

- import 부분의 g는 플라스크의 컨텍스트 변수이다. request 변수와 마찬가지로 [요청 → 응답] 과정에서 유효하다. 
- 코드에서 session 변수에 user_id값이 있으면 DB에서 사용자 정보를 조회해 g.user에 저장한다. 이후 사용자 로그인 검사할 때 session을 조사할 필요가 없다. g.user 값이 있는지만 확인하면 됨. 
- g.user에는 User 객체가 저장되어 있으므로 여러 가지 사용자 정보(username, email 등)를 추가로 얻어내는 이점이 있다.g.user에는 User 객체가 저장된다.


### 로그인 로그아웃 표시하기
- 네비게이션 바를 수정하자 {% if g.user %} 코드를 추가하여 사용자의 로그인 유무를 판별할 것
```html
<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Pybo</a>
        (... 생략 ...)
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            {% if g.user %}
            <ul class="navbar-nav">
                <li class="nav-item ">
                    <a class="nav-link" href="#">{{ g.user.username }} (로그아웃)</a>
                </li>
            </ul>
            {% else %}
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('auth.signup') }}">계정생성</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('auth.login') }}">로그인</a>
                </li>
            </ul>
            {% endif %}
        </div>
    </div>
</nav>

```
- 그인 했다면 g.user가 만들어진 상태이므로 username을 표시하고 "로그아웃" 링크를 보여 줄 것이다. 반대로 로그인을 하지 않았다면 "로그인"과 "계정생성" 링크를 보여 줄 것

### 로그아웃 라우팅 함수
- 로그아웃을 구현하기 위해 auth_views.py 파일을 열어 /logout/ URL에 매핑되는 logout 함수 작성
```python
(... 생략 ...)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
```
- logout 함수에는 세션의 모든 값을 삭제할 수 있도록 session.clear()를 추가했다. 따라서 session에 저장된 user_id는 삭제될 것이며, 앞서 작성한 load_logged_in_user 함수에서 session의 값을 읽을 수 없으므로 g.user도 None이 될 것

### 로그아웃 링크
- 링크 활성화하고 내비게이션바 수정


## 모델 수정하기
### SQLite 설정 수정하기
- SQLite 데이터베이스는 ORM을 사용할 때 몇 가지 문제점이 있다. 이것은 SQLite 데이터베이스에만 해당하고 PostgreSQL이나 MySQL 등의 다른 데이터베이스와는 상관없는 내용이다. 앞으로의 진행을 원활하게 하기 위해 SQLite가 발생시킬 수 있는 오류를 먼저 해결하고 넘어가야한다.
- ```init.py``` 수정

```python
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models
    (... 생략 ...)
```
- 수정하면 데이터베이스의 프라이머리 키, 유니크 키, 인덱스 키 등의 이름이 변경되므로 flask db migrate 명령과 flask db upgrade 명령으로 데이터베이스를 변경해야 한다.
- 데이터베이스에서 디폴트 값으로 명명되던 프라이머리 키, 유니크 키 등의 제약조건 이름을 수동으로 설정한 것

> SQLite 데이터베이스에서 사용하는 인덱스 등의 제약 조건 이름은 MetaData 클래스를 사용하여 규칙을 정의해야 한다. 만약 이름을 정의하지 않으면 SQLite 데이터베이스는 다음과 같은 제약 조건에 이름이 없다는 오류를 발생시킨다.
```ValueError: Constraint must have a name```
> QLite 데이터베이스는 ```migrate.init_app(app, db, render_as_batch=True)```처럼 render_as_batch 속성을 True로 지정해야 한다. 만약 이 속성이 False라면 다음과 같은 오류가 발생한다.
```ERROR [root] Error: No support for ALTER of constraints in SQLite dialectPlease refer to the batch mode feature which allows for SQLite migrations using a copy-and-move strategy.```
-init 파일에서 수정하내용은 SQLite 데이터베이스를 플라스크 ORM에서 정상으로 사용하기 위한 것 이라고 이해하면 됨


### Question 모델에 글쓴이 추가하기
- 누가 썼는지는 중요하니까
```models.py```
```python
(... 생략 ...)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
(... 생략 ...)
```

- user_id 속성은 User 모델을 Question 모델과 연결하기 위한 속성
- user 속성은 Question 모델에서 User 모델을 참조하기 위한 속성

#### 리비전 파일 생성,적용하기
- 모델 수정했으면 리비전 파일 생성하고 적용해야지
```
flask db migrate
flask db upgrade
```

- 리비전 파일 적용할 때 에러뜸
```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: _alembic_tmp_question.user_id
[SQL: INSERT INTO _alembic_tmp_question (id, subject, content, create_date) SELECT question.id, question.subject, question.content, question.create_date
FROM question]
(Background on this error at: http://sqlalche.me/e/gkpj)
```
- user_id가 Null을 허용하지 않기 때문,
- 실습을 진행하며 데이터베이스에 Question 모델 데이터를 여러 건 저장했던 것들은 user_id 속성의 값이 없다. 그런데 변경된 모델은 이를 허용하지 않으므로 오류가 발생한 것, 기존에 이미 저장되어 있던 데이터들 때문에 발생한 오류

### flask db upgrade 명령 오류 해결하기
1. user_id의 nullable 설정을 False 대신 True로 바꾸기
2. user_id를 임의의 값으로 설정하기(여기서는 1로 설정)
3. flask db migrate 명령, flask db upgrade 명령 다시 실행하기
4. user_id의 nullable 설정을 다시 False로 변경하기
5. flask db migrate 명령, flask db upgrade 명령 다시 실행하기

#### nullable=True
- user_id 속성의 nullable=False를 nullable=True로 변경하자. 그리고 user_id 속성의 기본값을 1로 설정하기 위해 server_default='1'을 입력
```models.py```
```python
(... 생략 ...)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('question_set'))
(... 생략 ...)

```
- server_default에 지정한 '1'은 최초로 생성한 User 모델 데이터의 id 값을 의미한다. 기존에 저장된 Question 데이터의 user_id값을 설정하기 위해서 server_default='1'이라는 속성을 추가
> server_default와 default의 차이
> erver_default를 사용하면 flask db upgrade 명령을 수행할 때 해당 속성을 갖고 있지 않던 기존 데이터에도 기본값이 저장된다. 하지만 default는 새로 생성되는 데이터에만 기본값을 생성함

#### 리비전 오류 확인
```flask db migrate```
```
ERROR [root] Error: Target database is not up to date.
```
- 이전 migrate 명령은 제대로 수행되었지만 upgrade를 실패해서 정상으로 종료되지 않았기 때문임

### 최종 리비전
```
flask db heads
a305d8f66479 (head)
```
### 현재 리비전
```
flask db current
bc15c419dc34
```

- 현재 시점의 리비전"과 "최종 리비전"이 같지 않다. 왜냐? upgrade를 실패했기 때문

### 현재 리비전을 최종 리비전으로 변경하기
- ```flask db stamp heads``` 명령을 사용하여 현재 리비전을 최종 리비전으로 되돌림
- ```flask db current``` 명령을 수행하면
- 현재(current) 리비전이 최종(head) 리비전으로 되돌려진 것을 확인할 수 있다. 이 작업은 마지막 수행했던 flask db migrate를 취소한 것

### 리비전 만들고 다시 적용
```
flask db migrate 
flask db upgrade
```
- 오류 없이 잘 수행된다. 이제 데이터베이스에는 Question 모델 데이터 모두 user_id 속성에 '1'이 저장된다.

### nullable=False
- id 속성에 1이 저장됐다면 다시 False로 바꿀 수 있다.server_default는 필요하지 않으므로 제거하자.
```python
(... 생략 ...)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
(... 생략 ...)
```
- 리비전 또 적용

## Answer 모델에 글쓴이 추가하기
- user_id 속성을 추가하자.
```python
(... 생략 ...)
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('answer_set'))
(... 생략 ...)
```
- 위처럼 또 반복임

## 질문, 답변 등록시 글쓴이 저장하기
### 답변 등록
```answer_views.py```
```
from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect
(... 생략 ...)

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)

```
- g 추가하자, 

### 질문 등록
```question_views.py```
```
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect
(... 생략 ...)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

```

### login_required
- 로그아웃 상태에서 질문 또는 답변을 등록하면 오류가 발생한다.
- 로그아웃 상태에서는 g.user의 값이 None이기 때문이다. 이 문제를 해결하려면 로그아웃 상태에서는 질문 또는 답변을 작성하려고 할 때 로그인을 먼저 진행할 수 있도록 로그인 페이지로 리다이렉트해야 한다
- 모든 질문, 답변 등록 함수의 시작 부분에 세션 값을 체크하여 사용자 정보가 없을 경우 로그인 페이지로 리다이렉트하는 코드를 추가해야 한다. 하지만 이런식으로 코드를 작성하면 코드가 중복되므로 무척 비효율적이다.

#### @login_required 데코레이터
- auth_views.py 파일에 login_required라는 이름의 데코레이터 함수를 다음과 같이 만들어 보자.

```auth_views.py```
```python
import functools

(... 생략 ...)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view
```
-  데코레이터 함수는 기존 함수를 감싸는 방법으로 간단히 만들 수 있다. 이제 라우팅 함수에 @login_required 애너테이션을 지정하면 login_required 데코레이터 함수가 먼저 실행될 것
- login_required 함수는 g.user가 있는지를 조사하여 없으면 로그인 URL로 리다이렉트 하고 g.user가 있으면 원래 함수를 그대로 실행할 것
- 요청 방식이 GET인 경우에는 로그인 후에 원래 가려던 페이지로 다시 찾아갈수 있도록 로그인 페이지에 next 파라미터를 전달했다. 따라서 로그인 함수도 next 파라미터를 처리하기 위해 다음과 같이 수정해야 한다.

```auth_views.py```
```python
(... 생략 ...)
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)
(... 생략 ...)    
```
- 로그인시 next 파라미터 값이 있으면 읽어서 로그인 후 해당 페이지로 이동하고 없으면 메인 페이지로 이동하게 했다.

### @login_required 적용하기
- 로그인에 필요한 함수에 @login_required 데코레이터를 적용해보자
- 질묺 함수에 등록해보자
```question_views.py```
```python
(... 생략 ...)
from pybo.views.auth_views import login_required

(... 생략 ...)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    (... 생략 ...)
```
- @login_required 데코레이터는반드시 함수명 바로 위에 위치해야한다. @login_required 데코레이터가 @bp.route 데코레이터보다 위에 위치할 경우 정상 작동하지 않는다.
- 답변을 등록하는 함수에도 적용해야함
```answer_views.py```
```python
(... 생략 ...)
from .auth_views import login_required
(... 생략 ...)

@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    (... 생략 ...)
```

### 로그아웃 상태에서 답변 등록 불가능하게 만들기
- 로그아웃 했을 때 답변을 쓸 수는 있다. 등록을 못할 뿐
- 등록하기 버튼 클릭시 해당 작성되던 화면에서 로그인 화면으로 넘어가면 작성된 답변이 날라간다.
- 아예 로그인을 못하면 답변을 입력을 못하게 하자.
```quetion_detail.html```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    (... 생략 ...)
    <form action="{{ url_for('answer.create', question_id=question.id) }}" method="post" class="my-3">
        (... 생략 ...)
        <div class="mb-3">
            <textarea {% if not g.user %}disabled{% endif %}
                    name="content" id="content" class="form-control" rows="10"></textarea>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary">
    </form>
</div>
{% endblock %}

```

- 문득 궁금해져서 당연하게도 if문이기에 앞에 두어야만 하는지에 대한 의문이 생겼다.
- 놀랍게도 뒤에 둬도 문제가 생기지 않았다. 그래서 찾아보니

> -disabled 속성의 위치는 HTML에서 중요하지 않다.
> -Jinja2 조건문을 앞에 두는 것은 가독성이나 관례 때문이지, 기능적인 이유 때문은 아니다.
> -어디에 두든 상관없지만, 앞에 두는 것이 더 명확하게 보일 수 있다.

- 가독성은 중요하니 늘 앞에 두도록하자.