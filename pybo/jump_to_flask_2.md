# 점프 투 플라스크
> 위키독스의 점프 투 플라스크를 참고해서 만들었습니다. 우분투 환경과 맞지 않거나 현재는 다른 부분을 조금 수정했습니다. 
> 2-06부터 시작합니다.

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
#### 실행하기
``` export FLASK_APP=pybo:create_app ``` 
- pybo 밖에서 터미널로 해당 명령어 실행
``` flask run ```
- flask 시작

## 답변 저장하기
- 답변을 입력할 텍스트 창과 <답변등록> 버튼을 생성하고, 이 버튼을 누르면 입력된 답변이 저장되게 구현
```question_detail.html```

```html
<h1>{{ question.subject }}</h1>
<div>
    {{ question.content }}
</div>
<form action="{{ url_for('answer.create', question_id=question.id) }}" method="post">
    <textarea name="content" id="content" rows="15"></textarea>
    <input type="submit" value="답변등록">
</form>
```
- 답변 저장 URL은 form 태그의 action 속성에 url_for('answer.create', question_id=question.id)로 지정했다. 이후 <답변등록> 버튼을 누르면 POST 방식으로 이 URL이 호출(submit)될 것
- 이 상태로 flask run하고 detail url로 진입하면 에러가 뜬다. 교재와 에러가 달라 당황했는데 찾아보니 answer 별칭에 해당하는 답변 블루프린트를 작성하지 않았고, create 라우팅 함수를 만들지 않았기 때문이다.

## 답변 블루 프린트 만들기
- views 디렉토리 안에 answer_views.py 파일만들고 내용 작성
```views/answer_views.py```

```python
from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    question = Question.query.get_or_404(question_id)
    content = request.form['content']
    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

```

### bp.route 애너테이션
- create 함수의 배개변수 question_id는 URL 매핑 규칙을 통해 전달된다. 
- ```http://locahost:5000/answer/create/[[MARK]]2[[/MARK]]/``` 페이지를 요청 받으면, question_id는 2를 넘겨 받음
- @bp.route의 메소드 속성에는 POST를 지정했다. 답변을 저장하는 질문 상세 템프릿의 form 엘리먼트가 POST 방식이므로, 같은 값을 지정해야한다. @bp.route에 똑같은 폼 방식을 지정하지 않으면 오류가 발생함.

### create 함수
- 템플릿의 form 엘리먼트를 통해 전달된 데이터들은 create 함수에서 request 객체로 얻을 수 있다.
- ```request.form['content']``` 코드는 POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 content인 값을 의미
- 마지막으로 ```__init__``` 파일을 수정하지 않으면 제대로 보이지 않는다.

### 답변 블루 프린트 등록
```
def create_app():
    (...생략...)

    # 블루프린트
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    return app
```
- ```init```파일을 수정하돌고하자.

### 답변 표시
- 답변 등록을 눌러도 아직 변하지 않는다. 등록된 답변을 화면에 표시하기 위해서 question_detail.html을 수정하자
```html
<h1>{{ question.subject }}</h1>
<div>
    {{ question.content }}
</div>
<h5>{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
<div>
    <ul>
    {% for answer in question.answer_set %}
        <li>{{ answer.content }}</li>
    {% endfor %}
    </ul>
</div>
<form action="{{ url_for('answer.create', question_id=question.id) }}" method="post">
    <textarea name="content" id="content" rows="15"></textarea>
    <input type="submit" value="답변등록">
</form>
```

- {{ question.answer_set|length }} 코드는 답변 개수를 의미한다. length는 템플릿 필터, 객체의 길이를 반환해 줌, 템플릿 필터는 | 문자뒤 추가해 사용한다.


## 화면 꾸미기
- 스타일시트를 이용해 웹 페이지에 디자인을 적용해보자
- css를 사용해야하는데 CSS파일이 pybo/static 디렉터리에 있어야함. CSS는 플라스크에서 static(정적으로 분류 된다, 이미지나 자바스크립트,스타일시트css 같은 파일을 의미함)

### 스태틱 디렉터리만들고 스타일 시트 작성
```/static/style.css```

```css
textarea {
    width:100%;
}
input[type=submit] {
    margin-top:10px;
}
```
- 텍스트 창 너비를 100%로 넓히고, 답변등록 버튼 위 마진을 10px 추가함. 너비 100%는 웹 브라우저 너비를 기준으로 함

### 질문 상세 화면에 스타일 시트 적용하기
- ```question_detail.html```
- 맨위 상단에 ```<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">``` 코드 추가
    - link rel : 연결하는 파일이 stylesheet 라는 뜻,
    - href : 연결할 파일의 경로를 명확하게 함, static 디렉토리의 style.css 파일이름을 가진 파일을 연결, url_for는 앞에서 URL 추적함수지만 정적 파일의 URL도 찾아줌



## 부트스트랩으로 편하게 화면 꾸미기
- https://getbootstrap.com/docs/5.1/getting-started/download/
- 해당 문서는 5버전을 기준으로 작성되었으며 다른 버전은 작동이 안될 수 있다.
- 해당 URL의 Compiled CSS and JS 밑 'Download' 버튼을 클릭하면 .zip 파일이 다운되는데 해당 파일의 압축을 풀고 css의 bootstrap.css를 복사해, 기존 프로젝트 폴더의 static에 집어넣자

### 질문 목록에 부트스트랩 적용하기
- question_list.html 파일 전체를 수정해야한다.
```html
<link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th>제목</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {% if question_list %}
        {% for question in question_list %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>
                <a href="{{ url_for('question.detail', question_id=question.id) }}">{{ question.subject }}</a>
            </td>
            <td>{{ question.create_date }}</td>
        </tr>
        {% endfor %}
        {% else %}
        <tr>
            <td colspan="3">질문이 없습니다.</td>
        </tr>
        {% endif %}
        </tbody>
    </table>
</div>
```
- 기존의 질문 목록은 엘리먼트로 간단히 표시했지만, table 엘리먼트로 변경, table 태그와 하위 태그들에 부스트스트랩 적용, class="contatiner my-3", class ="table", class = "table-dark" 등이 바로 부트스트랩이 제공하는 클래스
- 표가 예쁘게 꾸며지고, 반응형(모바일 등 다양한 화면 크기 지원)으로 동작함.
- <link rel="stylesheet" ...>로 CSS를 불러와야 하고, 각 요소에 부트스트랩 클래스(container, table, btn 등)를 붙여야 함
- CSS 적용이 잘 안되는 듯 하다면 css파일 이름을 확인하자 bootstrap.min 인거 멍때리면서 보다가 href 부분 보고 알게되었다.

### 질문 상세에 부트스트랩적용
```question_detail.html```

```html
<link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {{ question.create_date }}
                </div>
            </div>
        </div>
    </div>
    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
    {% for answer in question.answer_set %}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {{ answer.create_date }}
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
    <!-- 답변 등록 -->
    <form action="{{ url_for('answer.create', question_id=question.id) }}" method="post" class="my-3">
        <div class="mb-3">
            <textarea name="content" id="content" class="form-control" rows="10"></textarea>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary">
    </form>
</div>
```


|부트스트랩 클래스|	설명|
|------------|-----------------|
|card, card-body, card-text	|부트스트랩 Card 컴포넌트|
|badge	|부트스트랩 Badge 컴포넌트|
|form-control, form-label	|부트스트랩 Form 컴포넌트|
|border-bottom|	아래방향 테두리 선|
|my-3	|상하 마진값 3|
|py-2	|상하 패딩값 2|
|p-2	|상하좌우 패딩값 2|
|d-flex justify-content-end|	컴포넌트의 우측 정렬|
|bg-light	|연회색 배경|
|text-dark	|검은색 글씨|
|text-start	|좌측 정렬|
|btn btn-primary|	부트스트랩 버튼 컴포넌트|

## 표준 HTML과 상속 사용해보기
- 표준 HTML
```html
<!doctype html>
<html lang="ko">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
    <!-- pybo CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Hello, pybo!</title>
</head>
<body>
(... 생략 ...)
</body>
</html>
```
- html,head,body 엘리먼트가 있어야 하고,css파일 링크는 head안에 있어야 한다. head안에는 meta,title 엘리먼트 등이 포함되어야 한다.

## 템플릿을 표존 HTML로 바꾸기
- 표준 HTML로 바꾸면 CSS파일이 추가되거나 이름이 변경될 떄마다 파일 모두를 수정해야 하지만, 플라스크는 이런 불편함을 해소하기 위해 템플릿 상속 기능을 제공함, 이 기능 쓸 거임.

### 템플릿 파일의 기본 틀 작성하기 
- base.html을 작성해보자, 모든 템플릿에서 공통으로 입력할 내용을 여기에 포함한다.
```base.html```
```html
<!doctype html>
<html lang="ko">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
    <!-- pybo CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Hello, pybo!</title>
</head>
<body>
<!-- 기본 템플릿 안에 삽입될 내용 Start -->
{% block content %}
{% endblock %}
<!-- 기본 템플릿 안에 삽입될 내용 End -->
</body>
</html>
```

- body 엘리먼트에 {% block content %}와 {% endblock %} 템플릿 태그가 base.html 템플릿 파일을 상속한 템플릿에서 구현해야 할 영역임

#### 질문 목록 템플릿 수정
```question_list.html ```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <table class="table">
        (... 생략 ...)
    </table>
</div>
{% endblock %}
```
- base.html 템플릿 파일을 상속받고자 {% extends 'base.html' %} 템플릿 태그를 사용했다. 그리고 {% block content %}와 {% endblock %} 사이에 question_list.html에서만 사용할 내용을 작성한다.
- 원본 파일에서 맨 윗줄만 사라지긴 했다. 
- 기존의 link rel부분은 삭제하자 base.html이 css파일을 링크 했다.

#### 질문 상세 템플릿 파일 수정하기
- 이전 코드와 다를 것 없다. 맨 위 link rel 부분을 삭제 한 후 , 
```
{% extends 'base.html' %}
{% block content %}
(생략)
{% endblock %}
```

### 기존 스타일 파일 내용 비우기
- 부트스트랩을 쓰게 되었으니 style.css 파일의 내용을 비워두자


## 플라스크 폼 모듈로 데이터 검증 더 쉽게 하기
### 폼 모듈 설치하기
- ```Flask-WTF``` 라이브러리를 설치해야함
```pip install flask-wtf```
- 해당 라이브러리를 사용하려면 플라스크의 환경변수 SECRET_KEY가 필요함
> **SECRET_KEY** : 
SECRET_KEY는 CSRF(cross-site request forgery)라는 웹 사이트 취약점 공격을 방지하는 데 사용된다. CSRF는 사용자의 요청을 위조하는 웹 사이트 공격 기법인데 SECRET_KEY를 기반으로 해서 생성되는 CSRF 토큰은 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지를 판단해 주는 가늠자 역할을 한다.

- config.py 파일을 열고 마지막 줄에 SECRET_KEY 변수를 추가 해당 변수에 문자열을 입력해주자. 현재는 간단한 문자열을 넣고 이후에 실제 서비스에서 바꿔보자.



## 질문 등록 
- 모든 과정을 끝내야 제대로 동작함.
### 질문 등록 버튼 만들기
- question_list.html의 테이블 태그 아래에 질문 등록 버튼을 생성하자.
```html
(... 생략 ...)
    </table>
    <a href="{{ url_for('question.create') }}" class="btn btn-primary">질문 등록하기</a>
</div>
{% endblock %}
```

### 질문 폼 만들기 
- 질문 등록 URL을 추가했으니, question_view.py 파일에 라우팅 함수 create를 추가해야함, 그 전 질문 등록시 사용할 QuestionForm을 만들어야함 플라스크의 폼(Form)이다.
```forms.py```

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
```
- 글자수의 제한이 있는 "제목"의 경우 StringField를 사용
    - ```StringField('제목', validators=[DataRequired()])``` 에서 첫번째 입력인수인 "제목"은 폼 라벨(Label)이다. 템플릿에서 이 라벨을 이용하여 "제목"이라는 라벨을 출력할 수 있다.
    - 2번째 입력인수는 validators이다. validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length등이 있다. Ex) 필수값이면서 이메일이어야 하면 validators=[DataRequired(), Email()] 과 같이 사용할 수 있다.
- 글자수의 제한이 없는 "내용"은 TextAreaField를 사용


### 질문 등록 라우팅 함수 추가하기
- question_views.py 파일에 라우팅 함수 create를 추가하자.
```python
from pybo.forms import QuestionForm

(... 생략 ...)

@bp.route('/create/')
def create():
    form = QuestionForm()
    return render_template('question/question_form.html', form=form)
```
- 템플릿에 전달하는 form은 넴플릿에서 라벨이나 입력폼등을 만들 때 필요하다.

### 질문 등록 템플릿 작성하기
- templates/question 디렉터리에 question_form.html 파일생성 
```uestion_form.html```
```html
{% extends 'base.html' %}
{% block content %}
<!-- 질문 등록 -->
<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>
    <form method="post" class="my-3">

        {{ form.subject.label }}
        {{ form.subject() }}

        {{ form.content.label }}
        {{ form.content() }}

        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}
```
- 질문 등록을 위해서는 질문의 제목과 내용이라는 입력항목이 필요함. 위의 템플릿에서는 질문의 제목과 내용에 해당하는 입력 항목을 form 객체를 사용해서 만들었다. 
- {{ form.subject.label }} 는 라벨을 표시하고 {{ form.subject() }}는 입력폼을 표시

#### 질문 등록 기능 사용해보기
- flask run하고 질문 등록 따라서 계속 가면 ‘Method NotAllowed’ 오류 화면 뜬다.
- 현재 폼이 POST 방식으로 데이터를 전송하기 때문 ```question_form.html``` : ```<form method="post" class="my-3">```
- 태그에 post 속성을 지정했으므로 POST 방식으로 전송된다. create 라우팅 함수에는 별도의 method 속성을 지정하지 않아 기본 처리 방식인 GET 방식만 처리할 수 있다. create 함수의 라우팅 정보를 수정해야함
> 왜 form 태그에 action 속성(post,get같은)을 지정하지 않았기에 현재 페이지 URL의 디폴트 action으로 지정된다. 만약 action 속성을 지정하면 question_form.html 템플릿은 "질문 등록" 에서만 사용 가능하다. 질문 수정의 경우 또 새로운 템플릿을 여러개 만들어야하니까, action 속성은 비워두자.

### 질문 전송 방식 수정하기
- create 함수가 GET과 POST 모두 처리할 수 있도록 라우팅 데코레이션에 method 속성을 추가하자
```question_views```
```
@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    return render_template('question/question_form.html', form=form)
```
- 저장하기 버튼을 누르면 오류는 발생하지 않지만, 반응은 없다. create 함수가 미완성임, 폼 데이터 저장 코드 만들자

### 폼 데이터를 저장하는 코드 만들기
```question_views.py```
```python
from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from pybo import db
from ..models import Question
from ..forms import QuestionForm

(... 생략 ...)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

```
- if 문의 request.method는 create 함수로 요청된 전송 방식
- form.validate_on_submit 함수는 전송된 폼 데이터의 정합성을 점검한다. 즉, QuestionForm 클래스의 각 속성에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인
- POST 요청이고 폼 데이터에 이상이 없을 경우 질문을 저장한 뒤 main.index 페이지로 이동
- 폼으로부터 전달받은 "제목"에 해당하는 데이터는 form.subject.data로 얻고 있다. form.content.data도 마찬가지
- 코드의 핵심은 데이터 전송 방식이 POST인지 GET인지에 따라서 달리 처리하는 부분. 
- 질문 목록에서 <질문 등록하기> 버튼을 누르거나 질문 등록 화면에서 <저장하기> 버튼을 누르면 똑같이 /create/ 페이지를 요청하므로 create 함수가 요청을 받는다. create는 요청 방식을 구분해서 처리한다. 즉, <질문 등록하기> 버튼을 누르는 것은 GET 방식 요청이므로 질문 등록 화면을 보여 주고, <저장하기>버튼을 누르면 POST 방식 요청이므로 데이터베이스에 질문을 저장한다.

### 폼에 부스트랩 적용하기 
- {{ form.subject() }}와 같은 코드는 폼이 HTML을 자동으로 생성하므로 부트스트랩을 적용할 수 없다. 하지만 템플릿을 조금 수정하면 부트스트랩을 어느정도 적용할 수 있다.
``` question_form.html]```
```html
(... 생략 ...)
{{ form.subject.label }}
{{ form.subject(class="form-control") }}

{{ form.content.label }}
{{ form.content(class="form-control") }}
(... 생략 ...)
```
- 부트스트랩 클래스 class="form-control"을 적용할수 있다.

## 질문 등록 완성하기
### 오류 내용을 표시해 원인 알아내기
- 저장하기 눌러도 화면에 별 반응이 없으니, 이런 점을 보완하기 위해 오류 내용을 표시해보자
```question_form.html```
```html
(... 생략 ...)
    <form method="post" class="post-form my-3">
        <!-- 오류표시 Start -->
        {% if form.errors %}
        <div class="alert alert-danger" role="alert">
            {% for field, errors in form.errors.items() %}
            <strong>{{ form[field].label }}</strong>
            <ul>
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            </ul>
            {% endfor %}
        </div>
        {% endif %}
        <!-- 오류표시 End -->
        <div class="form-group">
(... 생략 ...)
```
- create함수에서 form.validate_on_submit() 코드가 실패(false 반환)하면 폼에는 오류 내용이 자동으로 등록 -> 등록된 오류는 form.errors 속성을 사용하여 위와 같이 표시할 수 있다.
- form.errors.items 의 field는 subject나 content와 같은 입력 폼의 필드를 의미함
- /create 에서 출력되는 문구를 보면 CSRF Token 오류가 난다. 전송된 데이터가 실제 웹 사이트에서 만들어진 데이터인지 검증하는 데 필요한 CSRF 토큰이 빠졌다는 의미

### CSRF 토큰 오류 처리하기
- form 태그 바로 밑에 {{ form.csrf_token }} 코드를 삽입하여 CSRF 토큰 오류에서 탈출해 보자.
```question_form ```
```
(... 생략 ...)
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>
    <form method="post" class="my-3">
        {{ form.csrf_token }}
        (... 생략 ...)
```

### 입력한 값 유지하고 오류 메시지 한글로 바꾸기
- 질문을 등록할 때 제목을 입력하고 내용 입력하지 않으면 오류 메시지가 뜨면서 입력한 제목이 사라진다. 이 문제를 해결해보자

#### 입력한 값ㅇ 유지하기
 ```question_form.html```
 ```html
 (... 생략 ...)
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" name="subject" id="subject"
                value="{{ form.subject.data or '' }}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" name="content"
                id="content" rows="10">{{ form.content.data or '' }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
(... 생략 ...)
```
- subject 필드의 value값으로 {{ form.subject.data or '' }}를 입력하면 이미 전송한 데이터가 다시 설정됨
- {{ form.subject.data or '' }}에서 or ''은 "현재 템플릿이 GET 방식으로 요청되는 경우 기존 입력값이 없으므로(None으로 출력) 이를 방지하기 위해서" 사용함. 
    - form.subject.data에 값이 없을 때 None이 아니라 ''이 출력된다. 
    - content필드에도 마찬가지 방법이 적용되었다.
- 내용도 입력하라는 오류가 표시되지만, 제목에 입력한 값이 더이상 사라지지 않는다.

#### 오류 메시지 한글로 바꾸기
- form.py를 바꿔주면 된다.
```forms```
```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
```

### 답변 등록에 폼 사용하기
- 답변 등록을 할 때 사용할 AnswerForm을 forms.py 파일에 추가하자.
- 답변에는 content 필드만 필요하다.
```Python
(... 생략 ...)

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
```

### 답변 등록 라우팅 함수 수정하기
- answer_views.py 파일에서 create 함수가 AnswerForm을 사용하게 변경
```Python 
from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)

```
- 답변 등록은 POST요청만 있으므로 GET, POST 분기처리는 필요없다.

### CSRF 코드와 오류 표시 기능 추가하기
```question_detail.html```
```html
(... 생략 ...)
    <form action="{{ url_for('answer.create', question_id=question.id) }}" method="post" class="my-3">
        {{ form.csrf_token }}
        <!-- 오류표시 Start -->
        {% if form.errors %}
        <div class="alert alert-danger" role="alert">
            {% for field, errors in form.errors.items() %}
            <strong>{{ form[field].label }}</strong>
            <ul>
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            </ul>
            {% endfor %}
        </div>
        {% endif %}
        <!-- 오류표시 End -->
        <div class="mb-3">
            <textarea name="content" id="content" class="form-control" rows="10"></textarea>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary">
(... 생략 ...)
```
- 질문 상세 템플릿에 폼이 추가되었으므로 question_views.py 파일의 detail 함수도 폼을 사용하도록 수정해야 한다. 이 과정이 없으면 템플릿에서 form 객체를 읽지 못해 오류가 난다.

```question_views.py```
```python
(... 생략 ...)
from ..forms import QuestionForm, AnswerForm
(... 생략 ...)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

(... 생략 ...)
```


# 파이보 서비스 개발!
- 이 장의 목표
1. 파이보를 상용 게시판 수준으로 본격적으로 개발한다.
2. 부트스트랩을 적용하여 서비스를 더 아름답게 만든다.
3. 게시물 등록, 삭제, 수정부터 로그인, 로그아웃, 페이징, 검색까지 게시판을 완벽하게 만든다.
## 내비게이션
### 내비게이션바 추가하기
- 모든 화면 위쪽에 고정되어 있는 부트스트랩 컴포넌트
- 편의기능 만들어보자. 
- 내비게이션 바는 모든 페이지에서 보여야 하므로 base.html 템플릿 파일을 열어 body 태그 아래 추가하자.
- 메인 페이지로 이동시켜주는 "Pybo" 로고 (클래스값 navbar-brand)를 가장 왼쪽에 배치하고, 오른쪽에는 계정생성과 로그인 링크를 추가
```base.html```
```html
<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Pybo</a>
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="#">계정생성</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
<!-- 기본 템플릿 안에 삽입될 내용 Start -->
```

### 부트스트랩이 제공하는 햄버거 메뉴 버튼 확인하기
- 브라우저 너비를 줄여보면 햄버거 메뉴 버튼이 생기고 계정생성과 로그인 버튼일 사라진다. (동작은 안한다)
- 부트스트랩은 작은 기기를 고려해 반응형 웹까지 적용되어 있음, 햄버거 버튼 작동 안하는 부트스트랩의 자바스크립트 파일이 base.html에 포함되어 있지 않기 때문, 아까 다운 받았던 Zip에서 꺼내오자 ``` bootstrap.min.js ```
- 추가적으로 base.html을 수정하면 햄버거메뉴 버튼을 누르면 숨어있는 링크가 표시됨
```html
<!-- 기본 템플릿 안에 삽입될 내용 End -->
<!-- Bootstrap JS -->
<script src="{{ url_for('static', filename='bootstrap.min.js') }}"></script>
```

### include 기능으로 내비게이션 바 추가해 보기
- 템플릿 특정 위치에 HTML을 삽입해 주는 기능이 있음, 
- 새롭게 파일을 생성하자

```pybo/templates/navbar.html```

```html
<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">Pybo</a>
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link" href="#">계정생성</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```
- navbar.html 파일의 코드는 base.html 파일에 작성했던 내비게이션 바를 위한 HTML을 그대로 복사한 것이다. 내비게이션 바와 관련된 코드를 분리했다.
- navbar.html 파일을 base.html 파일에 삽입해 보자.
```base```
```html
<!-- 네비게이션바 -->
{% include "navbar.html" %}
<!-- 기본 템플릿 안에 삽입될 내용 Start -->
```
- 기존의 nav 엘리먼트는 모두 삭제한다. 
- include 기능은 템플릿의 특정 영역을 중복, 반복해서 사용할 경우에 유용하다. 
- 중복, 반복하는 템플릿의 특정 영역을 따로 템플릿 파일로 만들고, include 기능으로 그 템플릿을 포함한다. 
- navbar.html 파일은 base.html 파일에서 1번만 사용되지만 따로 파일로 관리해야 이후 유지·보수하는 데 유리하므로 분리


## 게시판 페이징
### 임시 질문 300개 생성
- 플라스크 셸을 통해 질문을 만들어보자
```flask shell``` : 을 통해 진입 (까먹게 된다.)
```
>>> from pybo import db
>>> from pybo.models import Question
>>> from datetime import datetime
```
- For 문을 이용해 테스트 데이터 300개 설치
```
>>> for i in range(300):
...     q = Question(subject='테스트 데이터입니다:[%03d]' % i, content='내용무', create_date=datetime.now())
...     db.session.add(q)
... 
>>> db.session.commit()
```
- python에서 자동 들여쓰기가 될줄알고 조금 열받았는데 for문을 시작하면 다음 줄 부터는 tab을 누르고 보자
- 실행시켜 보면 끝 없는 스크롤 바를 볼 수 있다.

### 페이징 구현하기 
- views/question_views.py 파일을 열어 _list 함수에 다음처럼 페이징을 적용하자. 페이징은 paginate 함수를 사용하여 쉽게 구현할 수 있다.
```python
(... 생략 ...)
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

```
- Flask-SQLAlchemy 3.0 부터 paginate()함수가 키워드로만 인자를 보낼 수 있도록 변경되어 ```question_list = question_list.paginate(page, per_page=10)``` 대신 ```question_list = question_list.paginate(page=page, per_page=10)```으로 사용해야 한다.
- 1번째 인수로 전달된 page는 현재 조회할 페이지의 번호를 의미하고, 2번째 인수 per_page로 전달된 10은 페이지마다 보여 줄 게시물이 10건임을 의미함

|항목	|설명|	값의 예|
|---------|--------------|-------------|
|items	|현재 페이지에 해당하는 게시물 리스트	[<Question 282>,<Question 283>, ...]|
|total	|게시물 전체 개수	|302|
|per_page|	페이지당 보여 줄 게시물 개수|	10|
|page	|현재 페이지 번호	|2|
|iter_pages|	페이지 범위|	[1, 2, 3, 4, 5, None, 30, 31]|
|prev_num / next_num	|이전 페이지 번호 / 다음 페이지 번호	|현재 페이지가 3인 경우, 2 / 4|
|has_prev / has_next	|이전 페이지 존재 여부 / 다음 페이지 존재 여부	|True / False|

### 템플릿에 페이징 적용해 보기
#### 질문 목록 출력 코드 수정하기
```question_list.html```

```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <table class="table">
        (... 생략 ...)
        {% for question in question_list.items %}
        (... 생략 ...)
    </table>
    <a href="{{ url_for('question.create') }}" class="btn btn-primary">질문 등록하기</a>
</div>
{% endblock %}
```

### 페이지 이동 기능 추가로 페이징 기능 완성하기
- question_list.html 템플릿의 </table> 바로 아래에 다음과 같이 코드를 추가하자.
```html
(... 생략 ...)
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        {% if question_list.has_prev %}
        <li class="page-item">
            <a class="page-link" href="?page={{ question_list.prev_num }}">이전</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:void(0)">이전</a>
        </li>
        {% endif %}
        <!-- 페이지번호 -->
        {% for page_num in question_list.iter_pages() %}
        {% if page_num %}
        {% if page_num != question_list.page %}
        <li class="page-item">
            <a class="page-link" href="?page={{ page_num }}">{{ page_num }}</a>
        </li>
        {% else %}
        <li class="page-item active" aria-current="page">
            <a class="page-link" href="javascript:void(0)">{{ page_num }}</a>
        </li>
        {% endif %}
        {% else %}
        <li class="disabled">
            <a class="page-link" href="javascript:void(0)">...</a>
        </li>
        {% endif %}
        {% endfor %}
        <!-- 다음페이지 -->
        {% if question_list.has_next %}
        <li class="page-item">
            <a class="page-link" href="?page={{ question_list.next_num }}">다음</a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:void(0)">다음</a>
        </li>
        {% endif %}
    </ul>
    <!-- 페이징처리 끝 -->
    <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>
</div>
{% endblock %}

```
- 이전 페이지가 있는 경우에는 "이전" 링크가 활성화되게 하였고 이전 페이지가 없는 경우에는 "이전" 링크가 비활성화
- 페이지 리스트를 루프 돌면서 해당 페이지로 이동할 수 있는 링크를 생성
- 현재 페이지와 같을 경우에는 active클래스를 적용하여 강조표시

|페이징 기능|	코드|
|-----------|--------|
|이전 페이지가 있는지 체크	{% if question_list.has_prev %}|
|이전 페이지 번호|	{{ question_list.prev_num }}|
|다음 페이지가 있는지 체크|	{% if question_list.has_next %}|
|다음 페이지 번호|	{{ question_list.next_num }}|
|페이지 리스트 루프|	{% for page_num in question_list.iter_pages() %}|
|현재 페이지와 같은지 체크|	{% if page_num != question_list.page %}|

## 템플릿 필터 직접 만들어보기
- 템플릿에 | 를 붙여 필터링 수행
- 현재 질문 목록 템플릿에서는 datatime 객체를 문자열로 표시했음, 현재 2025-05-21 17:22:49.426871 이런식으로 출력되지만 이런 방식은 보통 쓰지 않는다.

### 템플릿 필터 만들기
- 이상하게 나오는 데이트 문자열을 바꿔보자
- filter.py 생성
```filter.py```

```python
def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    return value.strftime(fmt)
```
- format_datetime 함수는 전달받은 datetime 객체(value)를 날짜포맷형식(fmt)에 맞게 변환하여 리턴하는 함수
- fmt가 전달되지 않을 경우 디폴트 값인 '%Y년 %m월 %d일 %p %I:%M'이 사용


|항목|	설명|
|-------|--------|
|%Y|	년|
|%m	|월|
|%d|	일|
|%p	|AM, PM (오전, 오후의 구분)|
|%I	|시간 (0~12 시로 표현)|
|%M|	분|

### 앱에 필터 등록하기
- 필터를 템플릿에서 사용하려면 pybo/__init__.py 파일의 create_app 함수를 다음처럼 수정해야 한다.
```python
(... 생략 ...)
def create_app():
   (... 생략 ...)

    # 블루프린트
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    # 필터 해당 부분만 집어 넣으면 된다.
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
```
- format_datetime 함수를 임포트한 다음 app.jinja_env.filters['datetime']와 같이 datetime이라는 이름으로 필터를 등록

### 필터 사용해보기
```question_list.html```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <table class="table">
        (... 생략 ...)
        <tr>
            <td>{{ loop.index }}</td>
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

### 질문 상세 화면에 필터 적용하기
```question_detail.html```

```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {{ question.create_date|datetime }}
                </div>
            </div>
        </div>
    </div>
    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
    {% for answer in question.answer_set %}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {{ answer.create_date|datetime }}
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
(... 생략 ...)

```