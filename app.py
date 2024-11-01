from flask import Flask, render_template, request
import random

app = Flask(__name__)

# 질문 리스트
questions = [
    "나는 매일 과제나 업무 파일을 백업한다.",
    "교수님께서 답을 알려준다는 스팸 메일이라도 무조건 열어본다.",
    "노트북 카메라는 보통 가려둔다.",
    "자주 쓰는 비밀번호가 3개 이상 있다.",
    "스타벅스에서 공용 와이파이를 연결한다.",
    "포털사이트에 해킹 관련 뉴스가 보이면 종종 클릭해본다.",
    "인터넷 회원가입 시 개인정보 제공 동의 조항은 대충 읽고 넘긴다.",
    "랜섬웨어에 걸려도 본인은 걱정이 없다.",
    "컴퓨터, 핸드폰을 사용하면서 보안의 필요성을 느낀다.",
    "나는 동기가 보이스피싱에 걸려도 크게 상관없다.",
    "택배 수령 후 운송장은 찢어서 파기한다.",
    "보안 관련 세미나에 다녀왔다.",
    "내 개인 계정 또는 업무 관련 계정의 ID/비밀번호를 메모에 기록해둔다."
]

# 결과 유형 리스트
results = {
    "ISTJ": {
        "title": "철저한 보안 관리자 (ISTJ)",
        "description": "당신은 보안을 책임지는 최고의 관리자입니다. 규칙을 철저히 따르며, 모든 상황에서 시스템 안전성을 유지하는 것이 목표입니다.",
        "examples": "백업, 비밀번호 관리, 카메라 가리기",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/fJ3k2kC.jpg" alt="ISTJ 보안 관리자"/>'
    },
    "ENTP": {
        "title": "창의적인 보안 탐구자 (ENTP)",
        "description": "당신은 창의적이고 도전적인 보안 탐구자입니다. 최신 기술을 활용해 보안을 강화하고 새로운 시도를 즐깁니다.",
        "examples": "해킹 뉴스 클릭, 다양한 비밀번호 사용",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/Qapieu9.jpg" alt="ENTP 보안 탐구자"/>'
    },
    "ISFJ": {
        "title": "예방 중심 보안 수호자 (ISFJ)",
        "description": "당신은 조용하지만 강력한 보안 수호자입니다. 위협이 발생하기 전에 미리 준비하고, 예방하는 데 능숙합니다.",
        "examples": "개인정보 동의 조항 검토, 보안 경고 모니터링",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/3fFWKgG.jpg" alt="ISFJ 보안 수호자"/>'
    },
    "ESTP": {
        "title": "대응 전문가 (ESTP)",
        "description": "당신은 즉각적인 대응 전문가입니다. 보안 사고가 발생했을 때, 재빨리 대처하고 문제를 해결하는 데 능숙합니다.",
        "examples": "랜섬웨어 대응 방법 숙지, 공공 Wifi 사용",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/nKMFBqJ.jpg" alt="ESTP 대응 전문가"/>'
    },
    "INTP": {
        "title": "보안 혁신가 (INTP)",
        "description": "당신은 보안 혁신가입니다. 창의적인 방법을 통해 보안 문제를 해결하고, 항상 새로운 기술을 탐구합니다.",
        "examples": "다양한 비밀번호 사용, 최신 보안 뉴스 관심",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/2c0tHrE.jpg" alt="INTP 보안 혁신가"/>'
    },
    "ENTJ": {
        "title": "위험 감수형 (ENTJ)",
        "description": "당신은 위험을 감수하는 리더형 보안 전문가입니다. 대담하게 문제에 접근하며, 위기 상황에서도 침착하게 대응합니다.",
        "examples": "공공 Wifi 사용, 낯선 메일 열기",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/0O5LSPh.jpg" alt="ENTJ 위험 감수형"/>'
    },
    "ISFP": {
        "title": "안전 중심 보안 관리자 (ISFP)",
        "description": "당신은 조용하지만 안전을 책임지는 관리자입니다. 항상 위험을 방지하고 사람들의 데이터를 보호하는 데 최선을 다합니다.",
        "examples": "운송장 파기, 개인정보 보호 교육 참여",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/IHOE1DN.jpg" alt="ISFP 안전 중심 보안 관리자"/>'
    },
    "INFJ": {
        "title": "보안 철학자 (INFJ)",
        "description": "당신은 보안의 철학자입니다. 보안의 윤리적 문제와 사회적 책임에 대해 깊이 고민하며, 모두를 위한 더 나은 보안을 추구합니다.",
        "examples": "보안 정책 관심, 개인정보 보호 조항 검토",
        "image": '<img width="500" height="auto" src="https://i.imgur.com/5vK5tpM.jpg" alt="INFJ 보안 철학자"/>'
    },
    "NoInterest": {
        "title": "DOBBY",
        "description": "성:도 이름:비",
        "examples": "도비는 이제 자유에요>_<",
        "image": '<img width="1000" height="auto" src="https://i.imgur.com/1UdQC8R.jpg" alt="description"/>'
    }
}




def calculate_result(answers):
    # 모든 답이 'X'인지 확인
    if all(answer == 'no' for answer in answers):
        return "NoInterest"  

    # 각 유형에 대한 점수 초기화
    scores = {
        "ISTJ": 0,
        "ENTP": 0,
        "ISFJ": 0,
        "ESTP": 0,
        "INTP": 0,
        "ENTJ": 0,
        "ISFP": 0,
        "INFJ": 0
    }

    # 질문에 따른 가중치 및 점수 부여
    if answers[0] == 'yes':
        scores["ISTJ"] += 3 

    if answers[1] == 'yes':
        scores["ENTP"] += 3  
    
    if answers[2] == 'yes':
        scores["ISTJ"] += 2 
        scores["ISFJ"] += 1 
    
    if answers[3] == 'yes':
        scores["INTP"] += 2  
    
    if answers[4] == 'yes':
        scores["ENTJ"] += 3  
    
    if answers[5] == 'yes':
        scores["ENTP"] += 2  
        scores["INTP"] += 1  
    
    if answers[6] == 'yes':
        scores["ISFJ"] += 3  
    
    if answers[7] == 'yes':
        scores["ESTP"] += 3  
    
    if answers[8] == 'yes':
        scores["INFJ"] += 3  
    
    if answers[9] == 'yes':
        scores["ESTP"] += 2  
    
    if answers[10] == 'yes':
        scores["ISFP"] += 2  
        scores["ISTJ"] += 1  
    
    if answers[11] == 'yes':
        scores["ISTJ"] += 2  
    
    if answers[12] == 'yes':
        scores["ISFP"] += 2  
        scores["ISFJ"] += 1  
    
    max_score = max(scores.values())
    candidates = [key for key, value in scores.items() if value == max_score]
    
    result_type = random.choice(candidates)
    
    return result_type


@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = [request.form.get(f'q{i}') for i in range(1, len(questions) + 1)]
    result_type = calculate_result(answers)
    result = results[result_type]
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run()
