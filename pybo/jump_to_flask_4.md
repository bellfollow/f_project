# 점프 투 플라스크
> 위키독스의 점프 투 플라스크를 참고해서 만들었습니다. 실습하면서 제가 느낀점이나, 제 우분투 환경에서 조금 달랐던 것들을 수정했습니다. 
> 3-09부터 시작합니다.

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

# 글쓴이 표시하기
## 질문 목록에 글쓴이 표시하기
```question_list.html```
```python
(... 생략 ...)
<tr class="text-center table-dark">
    <th>번호</th>
    <th style="width:50%">제목</th>
    <th>글쓴이</th>
    <th>작성일시</th>
</tr>
(... 생략 ...)
```
- <th>글쓴이</th>를 추가, 가운데 정렬되게 tr 엘리먼트에 text-center 클래스를 추가하고 제목의 너비가 전체에서 50%를 차지하도록 style="width:50%"도 지정
- for문에도 글쓴이를 적용하자
```question_list.html```

```html
(... 생략 ...)
{% for question in question_list.items %}
<tr class="text-center">
    <td>{{ question_list.total - ((question_list.page-1) * question_list.per_page) - loop.index0 }}</td>
    <td class="text-start">
        <a href="{{ url_for('question.detail', question_id=question.id) }}">{{ question.subject }}</a>
        {% if question.answer_set|length > 0 %}
        <span class="text-danger small mx-2">{{ question.answer_set|length }}</span>
        {% endif %}
    </td>
    <td>{{ question.user.username }}</td>  <!-- 글쓴이 추가 -->
    <td>{{ question.create_date|datetime }}</td>
</tr>
{% endfor %}
(... 생략 ...)

```

- ```<td>{{ question.user.username }}</td>```를 삽입하여 질문의 글쓴이를 표시
- 테이블 내용을 가운데 정렬하도록 tr 엘리먼트에 text-center 클래스를 추가하고, 제목을 왼쪽 정렬하도록 text-start 클래스를 추가했다.

## 질문 상세에 글쓴이 표시하기
```question_detail.html```
```html
(... 생략 ...)
<div class="card-body">
    <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
    <div class="d-flex justify-content-end">
        <div class="badge bg-light text-dark p-2 text-start">
            <div class="mb-2">{{ question.user.username }}</div>
            <div>{{ question.create_date|datetime }}</div>
        </div>
    </div>
</div>
(... 생략 ...)
```
- 질문 상세 화면에도 질문 작성일시 바로 위에 글쓴이를 추가하자.
- 글쓴이와 작성일시를 함께 보여주도록 부트스트랩을 이용해 여백과 정렬 등의 디자인도 살짝 변경했다.
- 답변에도 글쓴이를 추가, 질문과 마찬가지로 작성일시 바로 위에 글쓴이를 표시하면됨
```question_detail.html```
```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<div class="card my-3">
  <div class="card-body">
      <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
      <div class="d-flex justify-content-end">
          <div class="badge bg-light text-dark p-2 text-start">
              <div class="mb-2">{{ answer.user.username }}</div>
              <div>{{ answer.create_date|datetime }}</div>
          </div>
      </div>
  </div>
(... 생략 ...)
```

# 게시물 수정 & 삭제
## 수정 일시
- 질문, 답변을 언제 수정했는지 확인할 수 있도록 Question 모델과 Answer 모델에 modify_date 속성을 추가
```models.py```
```python
from pybo import db

class Question(db.Model):
    (... 생략 ...)
    modify_date = db.Column(db.DateTime(), nullable=True)


class Answer(db.Model):
    (... 생략 ...)
    modify_date = db.Column(db.DateTime(), nullable=True)

(... 생략 ...)
```
- modify_date 속성에는 nullable=True로 null을 허용하도록 했다. 수정일시는 수정이 발생할 경우에만 생성되므로 null을 허용해야 한다.
- 모델 변경시 늘 하던 migrate와 upgrade 수행
```shell
flask db migrate
flask db upgrade
```
## 질문 수정
- 수정 버튼을 클릭해 수정 화면으로 진입

### 질문 수정 버튼
```question_detail.html```
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
        <div class="d-flex justify-content-end">
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{{ question.user.username }}</div>
                <div>{{ question.create_date|datetime }}</div>
            </div>
        </div>
        <div class="my-3">
            {% if g.user == question.user %}
            <a href="{{ url_for('question.modify', question_id=question.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            {% endif %}
        </div>
    </div>
</div>
(... 생략 ...)

```
- 질문 수정 버튼은 로그인한 사용자와 글쓴이가 같은 경우에만 보여야 하므로 {% if g.user == question.user %}를 사용했다.

## 질문 수정 라우팅 함수
- 질문 상세 템플릿에 ```url_for('question.modify', question_id=question.id)``` URL이 추가되었으니 다음과 같은 modify 함수를 작성하자
```question_views.py```
```python
(... 생략 ...)
from flask import Blueprint, render_template, request, url_for, g, flash

(... 생략 ...)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

```

- 질문 수정은 로그인이 필요하므로 @login_required 애너테이션을 추가함. 로그인한 사용자와 질문의 작성자가 다르면 수정할 수 없도록 falsh 오류를 발생시키는 코드도 추가했다.
> flash 함수는 강제로 오류를 발생시키는 함수로, 로직에 오류가 있을 때 사용함
- modify 함수가 GET 방식으로 요청되는 경우는 질문 수정 버튼을 눌렀을 때이다. 이때 수정할 질문에 해당하는 제목,내용 등의 데이터가 화면에 보여한다.
- DB에서 조회한 데이터를 템플릿에 적용하는 가장 간단한 방법은 QuestionForm(obj=question)과 같이 조회한 데이터를 obj 매개변수에 전달하여 폼을 생성하는 것이다. 이렇게 하면 QuestionForm의 subject, content 속성에 question 객체의 subject, content 값이 저장되어 화면에도 표시된다.

- modify 함수가 POST 방식으로 요청되는 경우는 질문 수정 화면에서 데이터를 수정한 다음 <저장하기> 버튼을 눌렀을 경우이다.
- form.validate_on_submit 함수에서 QuestionForm을 검증하고 아무 이상이 없으면 변경된 데이터를 저장한다. 
- 데이터 변경을 위해 입력한 form.populate_obj(question)는 form 변수에 들어 있는 데이터(화면에서 입력한 데이터)를 question 객체에 업데이트 하는 역할을 한다.

## 오류 표시
- flash에 의해 발생하는 수정권한이 없습니다. 오류가 질문 상세 화면 위쪽에 오류 영역을 추가하자
```question_detail.html```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <!-- flash 오류 -->
    {% for message in get_flashed_messages() %}
    <div class="alert alert-danger" role="alert">
        {{ message }}
    </div>
    {% endfor %}
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>
(... 생략 ...)
```
- 물론 수정은 로그인 한 사용자와 글 작성자가 동일한 경우에만 가능하기 때문에 이 오류가 표시될 일은 없을 것이다. 하지만 비 정상적인 방법으로 질문을 수정할 경우 오류를 보여주어야 하므로 필요한 부분이다.

## 질문 삭제
### 질문 삭제 버튼
```question_detail.html```
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        (... 생략 ...)
        <div class="my-3">
            {% if g.user == question.user %}
            <a href="{{ url_for('question.modify', question_id=question.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            <a href="javascript:void(0)" class="delete btn btn-sm btn-outline-secondary"
               data-uri="{{ url_for('question.delete', question_id=question.id) }}">삭제</a>
            {% endif %}
        </div>
    </div>
</div>
(... 생략 ...)
```
- 삭제버튼은 수정버튼과 달리 href 속성값을 "javascript:void(0)"
- href 속성값을 javascript:void(0)로 설정하면 해당 링크를 클릭해도 아무런 동작도 하지 않는다.
- 삭제를 실행할 URL을 얻기 위해 data-uri 속성을 추가하고, 삭제 버튼이 눌리는 이벤트를 확인할 수 있도록 class 속성에 delete 항목을 추가했다.
- data-uri 속성은 자바스크립트에서 클릭 이벤트 발생시 this.dataset.uri와 같이 사용하여 그 값을 얻을 수 있다.
- href에 삭제 URL을 직접 상요하지 않고 이러한 방식을 사용하는 이유는 삭제 버튼을 클릭했을 때 "정말로 삭제하시겠습니까?"와 같은 확인창이 필요하기 때문

### 자바스크립트
- 삭제 버튼을 눌렀을 때 확인창을 호출하기 위해서는 자바스크립트 코드가 필요하다.
- 일단 보자
```
<script type='text/javascript'>
const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
</script>
```
- 해당 코드의 의미는 delete라는 클래스를 포함하는 컴포넌트를 클릭하면 "정말 삭제하시곗습니까?"라는 질문을 하고 "확인을 선택했을 때, 해당 컴포넌트의 data-uri값으로 URL을 호출하라는 의미. 확인 대신 취소를 선택하면 아무런 일도 발생하지 않을 것
- 해당 클래스는 답변 삭제에도 사용됨
- 스크립트를 추가하면 삭제 버튼을 클릭하고 확인을 선택하면 data-uri 속성에 해당하는 ```{% url 'pybo:question_delete' question.id %}``` URL이 호출될 것

### 자바 스크립트 블록
- 자바스크립트는 HTML 구조에서 </body> 태그 바로 위에 삽입하는 것을 추천
- 이렇게 해야 화면 렌더링이 완료된 후에 자바스크립트가 실행됨, 화면 렌더링이 완료되지 않은 상태에서 자바스크립트를 실행하면 화면의 값을 읽지 못하는 오류가 발생할 수 있고, 화면 로딩이 지연되는 문제가 발생할 수 있다. 
```base.html```
```html
(... 생략 ...)
<!-- Bootstrap JS -->
<script src="{{ url_for('static', filename='bootstrap.min.js') }}"></script>
<!-- 자바스크립트 Start -->
{% block script %}
{% endblock %}
<!-- 자바스크립트 End -->
</body>
</html>
```
- base.html을 상속하는 템플릿들에서 content 블록을 구현하게 했던것과 마찬가지 방법으로 script 블록을 구현할수 있도록 했다.
- </body> 태그 바로 위에 ```{% block script %}{% endblock %}``` 블록을 추가했다. 이렇게 하면 이제 base.html을 상속하는 템플릿은 자바스크립트의 삽입 위치를 신경쓸 필요없이 스크립트 블록을 사용하여 자바스크립트를 작성하면 된다.

```question_detail.html``` 하단에 추가
```html
(... 생략 ...)
{% endblock %}
{% block script %}
<script type='text/javascript'>
const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
</script>
{% endblock %}
```

### 질문 삭제 라우팅 함수
- 질문 상세 템플릿에 작성한 data-uri 속성에 ```url_for('question.delete', question_id=question.id)``` URL이 추가되었으므로 질문을 삭제할 수 있도록 라우팅 함수 delete를 추가해야 한다.
```question_views.py```
```python
(... 생략 ...)
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
```
- 삭제 함수도 로그인이 필요하므로 @login_required 애너테이션을 적용함

## 답변 수정
- 답변 수정은 답변 등록 템플릿이 따로 없으므로 답변 수정에 사용할 템플릿이 추가로 필요함, 답변 등록은 수정용으로 사용하는 데는 적합하지 않음

### 답변 수정 버튼
```question_detail.html```

```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
        <div class="d-flex justify-content-end">
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{{ answer.user.username }}</div>
                <div>{{ answer.create_date|datetime }}</div>
            </div>
        </div>
        <div class="my-3">
            {% if g.user == answer.user %}
            <a href="{{ url_for('answer.modify', answer_id=answer.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            {% endif %}
        </div>
    </div>
</div>
{% endfor %}
(... 생략 ...)
```
### 답변 수정 라우팅 함수
- ```url_for('answer.modify', answer_id=answer.id)``` URL을 추가했으므로 answer_views.py 파일에 modify 함수를 추가
```python
(... 생략 ...)
from flask import Blueprint, url_for, request, render_template, g, flash

(... 생략 ...)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)

```

### 답변 수정 템플릿
```answer_form.html```
```html
<!-- 답변 수정 -->
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <h5 class="my-3 border-bottom pb-2">답변 수정</h5>
    <form method="post">
        {{ form.csrf_token }}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="content">답변내용</label>
            <textarea class="form-control" name="content" id="content"
                      rows="10">{{ form.content.data or '' }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}
```
- 질문과 마찬가지로 답변도 등록한 사용자와 로그인한 사용자가 같아야 수정 버튼이 나타난다 답변을 작상한뒤 수정 버튼을 누르면 답변 수정화면으로 이동한다. 정상적으로 동작하는지 확인해보자.


## 답변 삭제
### 답변 삭제 버튼
```question_detail.html```
```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<div class="card my-3">
    <div class="card-body">
        (... 생략 ...)
        <div class="my-3">
            {% if g.user == answer.user %}
            <a href="{{ url_for('answer.modify', answer_id=answer.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            <a href="#" class="delete btn btn-sm btn-outline-secondary "
               data-uri="{{ url_for('answer.delete', answer_id=answer.id) }}">삭제</a>
            {% endif %}
        </div>
    </div>
</div>
{% endfor %}
(... 생략 ...)

```
- <수정> 버튼 옆에 <삭제> 버튼을 추가했다. 질문의 <삭제> 버튼과 마찬가지로 <삭제> 버튼에 delete 클래스를 적용했으므로 <삭제> 버튼을 누르면 data-uri 속성에 설정한 url이 실행될 것

### 답변 삭제 라우팅 함수
- ```url_for('answer.delete', answer_id=answer.id)``` URL을 추가했으므로 answer_views.py 파일에 delete 함수를 작성하자.
```answer_views.py```
```python
(... 생략 ...)
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
```
- delete 함수 역시 로그인이 필요하므로 @login_required 애너테이션을 추가


## 수정일시 표시하기
```question_detail.html```
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
        <div class="d-flex justify-content-end">
            {% if question.modify_date %}
            <div class="badge bg-light text-dark p-2 text-start mx-3">
                <div class="mb-2">modified at</div>
                <div>{{ question.modify_date|datetime }}</div>
            </div>
            {% endif %}
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{{ question.user.username }}</div>
                <div>{{ question.create_date|datetime }}</div>
            </div>
        </div>
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
        <div class="d-flex justify-content-end">
            {% if answer.modify_date %}
            <div class="badge bg-light text-dark p-2 text-start mx-3">
                <div class="mb-2">modified at</div>
                <div>{{ answer.modify_date|datetime }}</div>
            </div>
            {% endif %}
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{{ answer.user.username }}</div>
                <div>{{ answer.create_date|datetime }}</div>
            </div>
        </div>
(... 생략 ...)
```

# 추천 기능 추가하기
## 모델 변경
- 질문이나 답변에 추천을 적용하려면 질문 모델과 답변 모델에 "추천인"이라는 속성을 추가해야한다. 하나의 질문에 여러명이 추천할 수 있고 한 명이 여러개의 질문에 추천할 수 있으므로 이런 경우 다대다 관계를 의미하는 ManyToMany 관계를 사용해야한다.

## question_voter
- SQLAlchemy에서 ManyToMany 관계를 적용하는 방법
```models.py```
```python
from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

(... 생략 ...)

```
- ManyToMany 관계를 적용하기 위해서는 db.Table을 통해 N:N 관계를 의미하는 테이블을 먼저 생성해야한ㄷ.
- question_voter는 사용자 id와 질문 id를 쌍으로 갖는 테이블 객체이다. 사용자 id와 질문 id가 모두 PK(프라이머리키)이므로 ManyToMany 관계가 성립된다.
- 해당 테이블은 다음과 같은 데이터가 만들어질 수 있다.

|user_id|	question_id|
|------------|----------------|
|1	|1|
|1|	2|
|1|	3|
|2|	1|
|2|	2|
|2|	3|

- 하나의 계정이 여러개의 질문을 가질 수 있고, 하나의 질문이 여러개의 계정을 가질 수 있음
- 중복된 데이터는 가질 수 없다.user_id와 question_id 는 프라이머리키이므로 두개의 값이 모두 같은 데이터는 저장될 수 없다.
- 프로그램에서 이렇게 중복된 데이터를 저장하려고 시도하면 데이터베이스 차원에서 오류가 발생할 것

## Question 모델에 voter 속성 추가하기
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
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
```
- voter는 추천인으로 User모델과 연결된 속성, secondary 값으로 위에서 생성한 question_voter 테이블 객체를 지정해 주었다. Question 모델을 통해 추천인을 저장하면 실제 데이터는 question_voter 테이블에 저장되고 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조할수 있게 된다.
- voter의 backref 이름은 question_voter_set 으로 지정해 주었다. 만약 어떤 계정이 a_user 라는 객체로 참조되었다면 a_user.question_voter_set 으로 해당 계정이 추천한 질문 리스트를 구할수 있다.
> backref의 이름은 중복될수 없다.
> relationship 속성 사용시 주의해야 할 점이 있다. 그것은 동일한 모델로 relationship 속성을 생성할때 backref 이름은 중복되면 안된다는 점, Question 모델에는 이미 User 모델과 연결한 user 속성에question_set 이라는 backref 이름이 존재하므로 voter 속성의 backref에는 question_set 이라는 이름을 사용할 수 없다.

### Answer 모델에 voter 속성 추가하기
```models.py```
```python
(... 생략 ...)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

(... 생략 ...)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
(... 생략 ...)
```

- db를 바꿨으니 적용시켜줘야한다.
```
flask db migrate
flask db upgrade
```

## 질문 추천
### 질문 추천 버튼 만들기
```question_detail.html```
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
        <div class="d-flex justify-content-end">
            (... 생략 ...)
        </div>
        <div class="my-3">
            <a href="javascript:void(0)" data-uri="{{ url_for('question.vote', question_id=question.id) }}"
               class="recommend btn btn-sm btn-outline-secondary"> 추천
                <span class="badge rounded-pill bg-success">{{ question.voter|length }}</span>
            </a>
            {% if g.user == question.user %}
            <a href="{{ url_for('question.modify', question_id=question.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            <a href="javascript:void(0)" class="delete btn btn-sm btn-outline-secondary"
               data-uri="{{ url_for('question.delete', question_id=question.id) }}">삭제</a>
            {% endif %}
        </div>
    </div>
</div>
(... 생략 ...)
```
- 질문의 추천 버튼을 질문의 수정 버튼 좌측에 추가했다. 그리고 버튼에는 추천수도 함께 보이도록 했다. 추천 버튼을 클릭하면 href의 속성이 javascript:void(0)으로 되어 있기 때문에 아무런 동작도 하지 않는다. 하지만 class 속성에 "recommend"를 추가하여 자바스크립로 data-uri에 정의된 URL이 호출되게 할 것, 추천 버튼을 눌렀을 때 확인창을 통해 사용자의 확인을 구하기 위함

#### 추천 스크립트
- 정말로 추천하시겠습니까 팝업을 띄위기 위해 코드 추가
```quetion_detail.html```
```html
(... 생략 ...)
{% block script %}
<script type='text/javascript'>
const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
const recommend_elements = document.getElementsByClassName("recommend");
Array.from(recommend_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 추천하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
</script>
{% endblock %}
```
- class="recommend"가 적용되어 있으므로 추천 버튼을 클릭하면 "정말로 추천하시겠습니까?"라는 질문이 나타나고 "확인"을 선택하면 data-uri 속성에 정의한 URL이 호출될 것

### 질문 추천 라우팅 함수
- ```url_for('question.vote', question_id=question.id)``` RL에 해당하는 라우팅 함수를 다음과 같이 추가하자.
```question_views.py```
```python
(... 생략 ...)
@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
```
- Question 모델의 vorter는 여러 사람을 추가할 수 있는 다대다 관계이므로 _question.voter.append(g.user)와 같이 append 함수로 추천인을 추가해야 한다.
- question_voter 테이블의 구조상 같은 사용자가 같은 질문을 여러 번 추천해도 추천 횟수는 증가하지 않는다. 동일한 사용자를 append 할때 오류가 날것 같지만 내부적으로 중복되지 않도록 잘 처리된다.

## 답변 추천
### 답변 추천 버튼 만들기

```question_detail.html```
```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
        <div class="d-flex justify-content-end">
            (... 생략 ...)
        </div>
        <div class="my-3">
            <a href="javascript:void(0)" data-uri="{{ url_for('answer.vote', answer_id=answer.id) }}"
               class="recommend btn btn-sm btn-outline-secondary"> 추천
                <span class="badge rounded-pill bg-success">{{ answer.voter|length }}</span>
            </a>
            {% if g.user == answer.user %}
            <a href="{{ url_for('answer.modify', answer_id=answer.id) }}"
               class="btn btn-sm btn-outline-secondary">수정</a>
            <a href="javascript:void(0)" class="delete btn btn-sm btn-outline-secondary "
               data-uri="{{ url_for('answer.delete', answer_id=answer.id) }}">삭제</a>
            {% endif %}
        </div>
    </div>
</div>
{% endfor %}
(... 생략 ...)

```

### 답변 라우팅 함수
- 답변 추천시 호출되는 url_for('answer.vote', answeri_d=answer.id) URL에 해당하는 라우팅 함수를 다음과 같이 추가하자.
```answer_views.py```
```python
(... 생략 ...)
@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=_answer.question.id))
```

# 앵커 
- 문제점이 있음
- 답글 작성, 수정 후 항상 페이지 상단으로 스크롤이 이동되어 본인이 작성한 답변을 확인하러 다시 스크롤 해야함. Ajax와 같은 비동기 방식으로 해결할 수 있지만 보다 더 쉬운 방법으로 해결하자
- HTML에는 URL 호출시 원하는 위치로 이동시켜 주는 앵커 태그가 있다.
- ex) HTML 중간에 <a id="flask"></a> 라는 앵커 태그가 있다면 이 HTML을 호출하는 URL 뒤에 #flask 라고 붙여주면 해당 페이지가 호출되면서 해당 앵커로 스크롤이 이동된다.

## 앵커 엘리먼트
```question_detail.html```
```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<a id="answer_{{ answer.id }}"></a>
<div class="card my-3">
(... 생략 ...)
```
- 답변이 반복되어 표시되는 for 문 바로 다음에 <a id="answer_{{ answer.id }}"></a>와 같이 앵커 엘리먼트를 추가했다. 앵커 엘리먼트의 id 속성은 유일해야 하므로 answer_{{ answer.id }}와 같이 답변 id를 사용했다.


## 앵커로 이동
- 답변을 등록하거나 수정할 때 위에서 지정한 앵커 태그로 이동하도록 코드를 수정하자. 다음은 답변 등록 또는 답변 수정을 한 뒤 사용했던 기존 코드의 일부이다.

```python
return redirect(url_for('question.detail', question_id=question_id))
```
- 엥커 엘리먼트를 포함하면 다음과 같다.
```python
return redirect('{}#answer_{}'.format(
    url_for('question.detail', question_id=question_id), answer.id))
```
- 리다이렉트 URL 뒤에 #answer_2와 같은 앵커를 추가하기 위해 format 함수를 사용했다. 이 방식으로 answer_views.py 파일의 create, modify, vote 함수를 수정하자.
```answer_views.py```
```python
(... 생략 ...)
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    (... 생략 ...)
    if form.validate_on_submit():
        (... 생략 ...)
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    (... 생략 ...)
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            (... 생략 ...)
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    (... 생략 ...)

(... 생략 ...)

@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    (... 생략 ...)
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))

(... 생략 ...)

```

# 마크다운 기능 적용하기
- 문법 아니까 바로 그냥 적용하는 법으로 넘어감 ㅎ

## 마크다운 설치
마크다운 기능을 추가하려면 마크다운 모듈을 설치해야 한다. 다음처럼 pip install flask-markdown으로 마크다운을 설치하자.
```shell
pip install flask-markdown
```

- 마크다운이 오류가 뜰 수 있다고 하니 만약 모듈 오류가 뜬다며는 git 저장소를 통해 flask-markdown 모듈을 업데이트 하자
```shell
pip install git+https://github.com/vanzhiganov/flask-markdown.git
```
- 과정에서 fatal: unable to connect to github.com:와 같은 오류가 발생할 경우에는 다음 명령을 수행한 후 다시 시도해 보자.
```shell
git config --global url."https://".insteadOf git://
```

## 마크다운 등록
- init.py에 app에 등록해야함
```python
(... 생략 ...)
from flaskext.markdown import Markdown
(... 생략 ...)

def create_app():
    (... 생략 ...)
    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app

```
- 마크다운에는 몇 가지 확장 기능을 사용함
- nl2br과 fenced_code : 마크다운 문법을 편하게 사용할 수 있도록 만들어 줌
    - nl2br은 줄바꿈 문자를 <br>로 바꿔 준다. 만약 이 확장 기능을 사용하지 않으면 원래 마크다운 문법인 줄끝에 스페이스를 2개 연속으로 입력해야 줄바꿈을 할 수 있다
    - fenced_code는 코드 표시 기능을 위해 추가했다.

## 마크다운 적용
- Flask-Markdown이 동작하도록 템플릿을 수정해 보자. 질문이 표시되는 HTML 부분만 약간 수정하면 됨
```question_detail.html```
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ question.content|markdown  }}</div>
        <div class="d-flex justify-content-end">
            (... 생략 ...)
```
- 기존의 ```style="white-space: pre-line;"```은 삭제하고 {{ question.content|markdown }}과 같이 markdown 필터를 적용했다.

```html
(... 생략 ...)
<!-- 답변 목록 -->
<h5 class="border-bottom my-3 py-2">{{ question.answer_set|length }}개의 답변이 있습니다.</h5>
{% for answer in question.answer_set %}
<a id="answer_{{ answer.id }}"></a>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ answer.content|markdown }}</div>
        <div class="d-flex justify-content-end">
            (... 생략 ...)
```

### MarkDown 설치 안됨 
- 당황스럽다 교재 따라했는데 안된다. import error뜨는데 일단 추가적인 해결방법은 찾았다.
1. 저장소 클론:
```bash
git clone https://github.com/vanzhiganov/flask-markdown.git
cd flask-markdown
```

2. 버전 수정:
- setup.py 파일에서 version='dev'를 유효한 버전(예: '0.3.1')으로 변경:
```python
# setup.py 19번째 줄 수정
setup(
    name='Flask-Markdown',
    version='0.3.1',  # 'dev' → '0.3.1'로 변경
    # ... 나머지 설정 유지
)
```

3. 수동 설치:
```bash
pip install .
```
- 만약 해결이 안됐다면...안타깝게 생각한다.


# 검색
- 검색기능은 필수다. 검색 기능을 위해서 DB를 공부해야한다고 하신다. 믿고 따르자

## 조인
- 작성자 이름이 홍길동인 질문을 검색할 수 있는 방법에 대해 생각해보자.
1. User 모델에서 username이 '홍길동'인 데이터의 id 조사하기
2. 1에서 조사한 id와 Question 모델의 user_id가 같은 데이터인지 조사하기
- 해당 절차를 코드로 구현하면
```shell
user = User.query.get(User.username=='홍길동')
Question.query.filter(Question.user_id==user.id)
```
- 조인을 사용하면 단계를 축소할 수 있다. ```Question.query.join(User).filter(User.username=='홍길동')```
- 조인은 일종의 교집합 역할을 한다.
## 아우터 조인
- 아우터 조인(OUTER JOIN)은 두 테이블을 조인할 때, 조인 조건에 맞지 않는 행도 결과에 포함시키는 조인 방식입니다.
- 즉, 한쪽 테이블에는 데이터가 있지만 다른 쪽에는 없는 경우에도, 기준이 되는 테이블의 데이터는 모두 결과에 나오고, 매칭되는 값이 없으면 NULL로 채웁니다

## 서브쿼리
- 답변 내용과 답변 작성자를 검색 조건에 포함하려면 단순 조인만으로는 복잡해질 수 있으므로, Answer와 User를 조인한 서브쿼리를 만든 뒤 Question과 아우터조인하는 것이 가독성과 성능 면에서 유리하다.

### 서브쿼리 작성
```python
sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
    .join(User, Answer.user_id == User.id).subquery()
```
→ 답변 내용(Answer.content), 답변 작성자(User.username), 질문 id(Answer.question_id)를 조회하는 서브쿼리 생성

### Question과 서브쿼리 아우터조인
```python
Question.query.outerjoin(sub_query, sub_query.c.question_id == Question.id)
```
→ Question과 서브쿼리를 question_id로 연결

### 검색 조건 추가 :
- 질문 제목, 질문 내용, 질문 작성자, 답변 내용, 답변 작성자 모두 OR 조건으로 검색 가능

```python
.filter(
    Question.subject.ilike(search) |
    Question.content.ilike(search) |
    User.username.ilike(search) |
    sub_query.c.content.ilike(search) |
    sub_query.c.username.ilike(search)
)
```

- 복잡한 검색 조건(답변 작성자 등)을 효율적으로 처리하려면,필요한 데이터만 모은 서브쿼리를 만들어 아우터조인하는 방식이 효과적이다.
## GET
- 검색 기능을 GET 방식으로 구현해야 하는 이유
- POST 방식으로 검색, 페이징 기능을 만들면 웹 브라우저에서 "새로고침" 또는 "뒤로가기"를 했을 때 "만료된 페이지" 오류를 종종 만난다. 
- POST 방식은 같은 POST 요청이 발생하면 중복을 방지하기 때문이다. 
    - 예를 들어 2페이지에서 3페이지로 갔다가 "뒤로가기"를 하면 2페이지로 갈 때 "만료된 페이지" 오류를 만날 수 있다. 이러한 이유로 게시판을 조회하는 목록 함수는 GET 방식을 사용해야 한다.


## 검색 기능 만들어 보기
### 검색 창
- 질문 목록 화면에 검색 창을 추가하자.
```question_list.html```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a href="{{ url_for('question.create') }}" class="btn btn-primary">질문 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" id="search_kw" class="form-control" value="{{ kw or '' }}">
                <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="button" id="btn_search">찾기</button>
                </div>
            </div>
        </div>
    </div>
    <table class="table">
    (... 생략 ...)
    </table>
    <!-- 페이징처리 시작 -->
    (... 생략 ...)
    <!-- 페이징처리 끝 -->
    <a href="{{ url_for('question.create') }}" class="btn btn-primary">질문 등록하기</a>
</div>
</html>
```
- ```<a href="{{ url_for('question.create') }}" class="btn btn-primary"> 질문 등록하기</a>``` 페이징 처리 끝 아래 의 이 부분삭제하자
- <table> 태그 상단 우측에 검색어를 입력할 수 있는 텍스트창을 생성하였다. 맨 밑에 있던 "질문 등록하기" 버튼은 검색 창의 좌측으로 이동했다. 그리고 자바 스크립트에서 이 텍스트창에 입력된 값을 읽기 위해 ```<input type="text" id="search_kw" class="form-control" value="{{ kw or '' }}">``` 추가한 점에 주목하자.

### 검색 폼
```quetion_list.html```
```html
(... 생략 ...)
    <!-- 페이징처리 끝 -->
</div>
<form id="searchForm" method="get" action="{{ url_for('question._list') }}">
    <input type="hidden" id="kw" name="kw" value="{{ kw or '' }}">
    <input type="hidden" id="page" name="page" value="{{ page }}">
</form>
{% endblock %}
```
- GET 방식으로 요청해야 하므로 method 속성에 "get"을 설정했다. 
- kw와 page는 이전에 요청했던 값을 기억해야 하므로 value 속성에 그 값을 대입했다. 
- kw와 page의 값은 목록 조회 함수에서 전달할 것이다. form 엘리먼트의 action 속성은 "폼이 전송되는 URL"이므로 목록 조회 URL인 url_for('question._list')를 지정했다.

### 페이징
- 기존의 페이징도 ?page=1 에서 값을 읽어 요청하는 방식으로 변경해야 한다. 왜냐하면 검색과 페이징이 동시 처리되려면 위에서 작성한 form을 통해 페이징이 요청되어야 하기 때문
```html
(... 생략 ...)
<!-- 페이징처리 시작 -->
<ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    {% if question_list.has_prev %}
    <li class="page-item">
        <a class="page-link" data-page="{{ question_list.prev_num }}" href="javascript:void(0)">이전</a>
    </li>
    {% else %}
    <li class="page-item disabled">
        <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:void(0)">이전</a>
    </li>
    {% endif %}
    {% for page_num in question_list.iter_pages() %}
    {% if page_num %}
    {% if page_num != question_list.page %}
    <li class="page-item">
        <a class="page-link" data-page="{{ page_num }}" href="javascript:void(0)">{{ page_num }}</a>
    </li>
    {% else %}
    <li class="page-item active" aria-current="page">
        <a class="page-link" href="#">{{ page_num }}</a>
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
        <a class="page-link" data-page="{{ question_list.next_num }}" href="javascript:void(0)">다음</a>
    </li>
    {% else %}
    <li class="page-item disabled">
        <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:void(0)">다음</a>
    </li>
    {% endif %}
</ul>
<!-- 페이징처리 끝 -->
(... 생략 ...)

```
- 모든 페이지 링크를 href 속성에 직접 입력하는 대신 data-page 속성으로 값을 읽을 수 있도록 변경했다.

### 검색 스크립트
- 이징과 검색을 요청하는 자바스크립트 코드를 다음과 같이 추가
```question_list.html```
```html
(... 생략 ...)
{% endblock %}
{% block script %}
<script type='text/javascript'>
const page_elements = document.getElementsByClassName("page-link");
Array.from(page_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        document.getElementById('page').value = this.dataset.page;
        document.getElementById('searchForm').submit();
    });
});
const btn_search = document.getElementById("btn_search");
btn_search.addEventListener('click', function() {
    document.getElementById('kw').value = document.getElementById('search_kw').value;
    document.getElementById('page').value = 1;  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
    document.getElementById('searchForm').submit();
});
</script>
{% endblock %}
```
- class 속성값으로 "page-link"라는 값을 가지고 있는 링크를 클릭하면 
```<a class="page-link" data-page="{{ page_num }}" href="javascript:void(0)">{{ page_num }}</a>```
- 이 링크의 data-page 속성값을 읽어 searchForm의 page 필드에 설정하여 searchForm을 요청하도록
```javascript
const page_elements = document.getElementsByClassName("page-link");
Array.from(page_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        document.getElementById('page').value = this.dataset.page;
        document.getElementById('searchForm').submit();
    });
});
```
- 색버튼을 클릭하면 검색어 텍스트창에 입력된 값을 searchForm의 kw 필드에 설정하여 searchForm을 요청하도록 다음과 같은 스크립트를 추가
```javascript
const btn_search = document.getElementById("btn_search");
btn_search.addEventListener('click', function() {
    document.getElementById('kw').value = document.getElementById('search_kw').value;
    document.getElementById('page').value = 1;  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
    document.getElementById('searchForm').submit();
});
```

## 검색 함수
```question_views.py```
```python
(... 생략 ...)
from ..models import Question, Answer, User

(... 생략 ...)

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \             
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \            
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

(... 생략 ...)
```