/**
 * mathedu-quest-game.js
 * =====================
 * 👑 [수능 수학 100점 만점 원정대: CSAT 100-Point Perfect Score Quest]
 * - 수석 수학 교사 에이전트(mathteacher)와 공동 설계한 초등 기초 직관 ➔ 수능 수학 100점 만점 정복 인터랙티브 RPG/탐험 게임
 * - 연동 자원:
 *   1. mathedu 전체 16,548문항 (212개 단독 디딤돌 퀴즈 + 2006~2026 전 연도 기출 샤드 DB 실시간 소환)
 *   2. 민은기 선생님의 수학자료실 (https://min7014.github.io/) 3,400+ 시각적 기하 증명·GeoGebra·PDF 비급서
 *   3. 초등 눈높이 디딤돌 보호막 (0단계 기호 번역기 ➔ 1단계 초등 직관 ➔ 2단계 공식 브릿지 ➔ 3·4단계 수식 빈칸 (가)·(나) ➔ 5단계 본문항 격파)
 */

(function(window) {
  'use strict';

  var QUEST_STATE_KEY = 'mathedu_csat100_quest_v1';

  // 6대 탐험 월드 및 대표 보스·스테이지 데이터 (mathteacher 교육과정 설계 명세 반영)
  var WORLDS = [
    {
      id: 'w1',
      num: 1,
      icon: '🌱',
      name: '제1대륙 · 고1 공통수학 기초 왕국',
      sub: '다항식 · 방정식 · 원과 직선 · 도형의 이동 (목표: 0점 ➔ 18점)',
      targetScore: 18,
      emblemId: 'emblem_w1',
      emblemName: '🏅 고1 기초의 방패',
      shardYears: ['2025', '2024', '2023'],
      shardGrade: '고1',
      shardKeywords: ['다항식', '이차방정식', '이차함수', '원의 방정식', '도형의 이동', '집합'],
      teacherAdvice: '수능 수학 100점의 뿌리는 고1 공통수학의 도형과 함수 이동에 있습니다! 구구단과 넓이 직관에서 출발해 원과 직선의 위치 관계를 정복해 볼까요?',
      min7014Links: [
        { title: '📐 (a+b)²=a²+2ab+b² 시각적 넓이 퍼즐 (GeoGebra)', url: 'https://www.geogebra.org/m/bc3bfxgz', type: 'GeoGebra' },
        { title: '🪞 평면의 대칭·반사 이동 실험 (GeoGebra)', url: 'https://www.geogebra.org/m/xqcwgqwb', type: 'GeoGebra' },
        { title: '📘 곱셈공식과 도형의 이동 시각적 증명 아카이브', url: 'https://min7014.github.io/math20190821001.html', type: 'Archive' }
      ],
      stages: [
        {
          id: 'w1_s1',
          slug: 'c1092101',
          url: 'board/c1092101.html',
          gradeBadge: '4점 보스 · 고1 9월 학평 21번',
          bossName: '🛡️ 원과 직선 최댓값의 수호자',
          scoreReward: 9,
          xpReward: 60,
          symbols: [
            { sym: '$(x-a)^2+(y-b)^2=r^2$', desc: '중심이 $(a,b)$이고 반지름이 $r$인 동그란 원 위의 점들의 약속' },
            { sym: '$d = \\dfrac{|ax_1+by_1+c|}{\\sqrt{a^2+b^2}}$', desc: '원의 중심에서 직선까지 수직으로 잰 가장 짧은 거리' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 직관 타격] 직각삼각형 피타고라스 변의 길이',
              know: '초등학교·중학교 도형에서 직각삼각형의 밑변이 $3$, 높이가 $4$이면 가장 긴 빗변의 길이는 $\\sqrt{3^2+4^2}=\\sqrt{25}=5$입니다.',
              stem: '직각삼각형에서 직각을 낀 두 변의 길이가 $3$과 $4$일 때, 빗변의 길이는 얼마인가요?',
              options: ['$3$', '$4$', '$5$', '$6$', '$7$'],
              answer: 3,
              exp: '$3^2 + 4^2 = 9 + 16 = 25 = 5^2$이므로 빗변의 길이는 $5$입니다.'
            },
            {
              stepNum: 2,
              label: '🌿 2단계 · [기호 번역 브릿지] 원 위의 점에서 직선까지의 최대 거리',
              know: '원의 중심에서 직선까지의 거리를 $d$, 원의 반지름을 $r$이라 할 때, 원 위의 점에서 직선까지 가장 멀리 떨어진 거리는 중심 거리에 반지름을 더한 $d + r$입니다.',
              stem: '원의 중심과 직선 사이의 거리가 $d=5$이고 원의 반지름이 $r=2$일 때, 원 위의 점에서 직선까지의 거리의 최댓값 $d+r$은?',
              options: ['$3$', '$5$', '$7$', '$10$', '$12$'],
              answer: 3,
              exp: '중심에서 직선까지의 거리 $5$에 반지름 $2$만큼 더 멀어질 수 있으므로 최댓값은 $5 + 2 = 7$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [보스 격파] 원과 직선 위치 관계 마스터 확인',
              know: '원의 중심에서 직선까지의 거리 $d$와 반지름 $r$을 구해 더하면 최댓값 $M=d+r$, 빼면 최솟값 $m=d-r$이 됩니다.',
              stem: '원의 중심에서 직선까지의 거리가 $d=4\\sqrt{2}$이고 반지름이 $r=\\sqrt{2}$일 때, 최댓값 $M=d+r$과 최솟값 $m=d-r$의 곱 $M \\times m$의 값은?',
              options: ['$24$', '$26$', '$28$', '$30$', '$32$'],
              answer: 4,
              exp: '$M = 5\\sqrt{2}$, $m = 3\\sqrt{2}$이므로 $M \\times m = 5\\sqrt{2} \\times 3\\sqrt{2} = 15 \\times 2 = 30$입니다.'
            }
          ]
        },
        {
          id: 'w1_s2',
          slug: 'c2092102',
          url: 'board/c2092102.html',
          gradeBadge: '4점 보스 · 고2 9월 학평 21번',
          bossName: '⚔️ 이차함수와 대칭이동의 파수꾼',
          scoreReward: 9,
          xpReward: 60,
          symbols: [
            { sym: '$y = f(x-p)+q$', desc: '그래프 모양은 그대로 두고 오른쪽으로 $p$칸, 위로 $q$칸 옮기는 평행이동 약속' },
            { sym: '$x = -\\dfrac{b}{2a}$', desc: '이차함수 $y=ax^2+bx+c$ 포물선을 반으로 접는 대칭축의 위치' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 수직선 직관] 한가운데(중점) 숫자 찾기',
              know: '수직선에서 두 수 $2$와 $8$의 정가운데 있는 수는 두 수를 더해 $2$로 나눈 $\\frac{2+8}{2}=5$입니다.',
              stem: '수직선 위에서 두 점 $2$와 $10$의 정가운데(중점)에 위치한 숫자는?',
              options: ['$4$', '$5$', '$6$', '$7$', '$8$'],
              answer: 3,
              exp: '두 수의 합을 $2$로 나누면 $\\dfrac{2+10}{2} = 6$입니다.'
            },
            {
              stepNum: 2,
              label: '🌿 2단계 · [기호 번역 브릿지] 이차함수의 대칭축과 두 근의 합',
              know: '이차함수 $y=(x-2)(x-10)$의 그래프는 좌우 대칭이므로, $x$축과 만나는 두 점 $2$와 $10$의 정가운데인 $x=6$이 대칭축입니다.',
              stem: '대칭축이 $x=6$인 이차함수 $y=f(x)$에 대하여 $f(x)=0$의 두 실근 $\\alpha, \\beta$의 합 $\\alpha + \\beta$는?',
              options: ['$6$', '$8$', '$10$', '$12$', '$16$'],
              answer: 4,
              exp: '두 근의 중점이 대칭축 $6$이므로 $\\dfrac{\\alpha+\\beta}{2}=6$, 즉 $\\alpha+\\beta = 12$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [보스 격파] 평행이동된 그래프의 교점 합 구하기',
              know: '그래프를 $x$축 방향으로 $3$만큼 평행이동하면 대칭축도 $x=6$에서 $x=6+3=9$로 이동합니다.',
              stem: '대칭축이 $x=9$로 이동한 이차함수 그래프가 $x$축과 만나는 두 점의 $x$좌표의 합은?',
              options: ['$9$', '$12$', '$15$', '$18$', '$21$'],
              answer: 4,
              exp: '새로운 대칭축이 $x=9$이므로 두 교점의 중점이 $9$가 되어 두 좌표의 합은 $2 \\times 9 = 18$입니다.'
            }
          ]
        }
      ]
    },
    {
      id: 'w2',
      num: 2,
      icon: '🔥',
      name: '제2대륙 · 수학Ⅰ 지수·로그·삼각·수열 왕국',
      sub: '거듭제곱근 · 로그 · 사인·코사인법칙 · 수열의 합 (목표: 18점 ➔ 45점)',
      targetScore: 45,
      emblemId: 'emblem_w2',
      emblemName: '🔥 초월함수와 수열의 인장',
      shardYears: ['2026', '2025', '2024'],
      shardGrade: '고3',
      shardKeywords: ['지수', '로그', '삼각함수', '사인법칙', '코사인법칙', '등차수열', '등비수열', '수열의 합'],
      teacherAdvice: '수능 공통과목 전반부(수학Ⅰ)는 지수·로그의 밑 통일, 사인·코사인법칙의 외접원 작도, 그리고 수열의 규칙 찾기가 핵심입니다!',
      min7014Links: [
        { title: '📐 삼각함수 단위원과 사인·코사인법칙 기하 증명', url: 'https://min7014.github.io/', type: 'Archive' },
        { title: '📊 등차·등비수열의 계단식 합 시각화 자료', url: 'https://www.geogebra.org/u/min7014', type: 'GeoGebra' }
      ],
      stages: [
        {
          id: 'w2_s1',
          slug: 'csat26_01',
          url: 'board/csat26_01.html',
          gradeBadge: '2점 정찰병 · 2026학년도 수능 공통 1번',
          bossName: '⚡ 유리수 지수법칙의 문지기',
          scoreReward: 9,
          xpReward: 45,
          symbols: [
            { sym: '$(a^m)^n = a^{mn}$', desc: '거듭제곱의 거듭제곱은 지수끼리 곱하는 약속' },
            { sym: '$a^m \\times a^n = a^{m+n},\\; a^0 = 1$', desc: '밑이 같을 때 곱셈은 지수끼리 더하고, 지수가 $0$이면 항상 $1$이 되는 약속' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 구구단 직관] 9는 3을 몇 번 곱한 수일까?',
              know: '구구단에서 $3 \\times 3 = 9$이므로 $9$를 밑이 $3$인 거듭제곱으로 쓰면 $3^2$입니다.',
              stem: '$9 = 3^k$에서 지수 $k$에 알맞은 수는?',
              options: ['$1$', '$2$', '$3$', '$4$', '$5$'],
              answer: 2,
              exp: '$3 \\times 3 = 9$이므로 $9 = 3^2$, 즉 $k=2$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [수식 빈칸 (가) 공략] 밑을 3으로 통일하기',
              know: '주어진 식 $9^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$에서 $9 = 3^2$을 대입하여 정리합니다.',
              stem: '식 $9^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}} = [\\;\\text{(가)}\\;]$에서 빈칸 $[\\;\\text{(가)}\\;]$에 들어갈 알맞은 식은?',
              options: [
                '$(3^2)^{\\frac{1}{4}} \\times 3^{-\\frac{1}{3}}$',
                '$(3^2)^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$',
                '$(3^3)^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$',
                '$(3^2)^{\\frac{1}{2}} \\times 3^{-\\frac{1}{4}}$',
                '$(3^4)^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$'
              ],
              answer: 2,
              exp: '$9 = 3^2$이므로 $9^{\\frac{1}{4}} = (3^2)^{\\frac{1}{4}}$이 되어 $(3^2)^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 1번 본문항 격파] $9^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$의 값',
              know: '$(3^2)^{\\frac{1}{4}} = 3^{\\frac{2}{4}} = 3^{\\frac{1}{2}}$이므로 $3^{\\frac{1}{2}} \\times 3^{-\\frac{1}{2}} = 3^{\\frac{1}{2}-\\frac{1}{2}} = 3^0$입니다.',
              stem: '[2026학년도 수능 공통 1번] $9^{\\frac{1}{4}} \\times 3^{-\\frac{1}{2}}$의 값은? [2점]',
              options: ['$1$', '$\\sqrt{3}$', '$3$', '$3\\sqrt{3}$', '$9$'],
              answer: 1,
              exp: '$3^{\\frac{1}{2}} \\times 3^{-\\frac{1}{2}} = 3^0 = 1$이므로 정답은 1번($1$)입니다.'
            }
          ]
        },
        {
          id: 'w2_s2',
          slug: 'csat26_03',
          url: 'board/csat26_03.html',
          gradeBadge: '3점 정예 · 2026학년도 수능 공통 3번',
          bossName: '🔢 시그마(∑) 합의 수호자',
          scoreReward: 9,
          xpReward: 55,
          symbols: [
            { sym: '$\\sum_{k=1}^{4} a_k = a_1+a_2+a_3+a_4$', desc: '$k=1$부터 $4$까지 차례대로 넣어 모두 더하라는 기호' },
            { sym: '$\\sum_{k=1}^{n} (2a_k - k) = 2\\sum_{k=1}^{n} a_k - \\sum_{k=1}^{n} k$', desc: '시그마 안의 덧셈·뺄셈과 상수배는 각각 쪼개서 계산할 수 있는 성질' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 덧셈 직관] 1부터 4까지 자연수의 합',
              know: '$\\sum_{k=1}^{4} k$는 $1 + 2 + 3 + 4$를 줄여 쓴 기호입니다.',
              stem: '초등학교 덧셈 $1 + 2 + 3 + 4 = \\sum_{k=1}^{4} k$를 계산한 값은?',
              options: ['$6$', '$8$', '$10$', '$12$', '$15$'],
              answer: 3,
              exp: '$1 + 2 + 3 + 4 = 10$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [수식 빈칸 (가) 공략] 시그마 성질로 식 분리하기',
              know: '$\\sum_{k=1}^{4}(2a_k - k) = 0$에서 시그마를 분리하면 $2\\sum_{k=1}^{4}a_k - \\sum_{k=1}^{4}k = 0$입니다.',
              stem: '$\\sum_{k=1}^{4} k = 10$을 대입할 때, $2\\sum_{k=1}^{4} a_k - [\\;\\text{(가)}\\;] = 0$의 빈칸 $[\\;\\text{(가)}\\;]$에 들어갈 수는?',
              options: ['$4$', '$6$', '$8$', '$10$', '$12$'],
              answer: 4,
              exp: '$\\sum_{k=1}^{4} k = 10$이므로 $2\\sum_{k=1}^{4} a_k - 10 = 0$이 됩니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 3번 본문항 격파] $\\sum_{k=1}^{4} a_k$의 값 구하기',
              know: '$2\\sum_{k=1}^{4} a_k = 10$의 양변을 $2$로 나누면 목표값을 얻습니다.',
              stem: '[2026학년도 수능 공통 3번] 수열 $\\{a_n\\}$에 대하여 $\\sum_{k=1}^{4}(2a_k - k) = 0$일 때, $\\sum_{k=1}^{4} a_k$의 값은? [3점]',
              options: ['$1$', '$2$', '$3$', '$4$', '$5$'],
              answer: 5,
              exp: '$2\\sum_{k=1}^{4} a_k = 10 \\implies \\sum_{k=1}^{4} a_k = 5$ (정답 5번)입니다.'
            }
          ]
        },
        {
          id: 'w2_s3',
          slug: 'c30910',
          url: 'board/c30910.html',
          gradeBadge: '4점 준킬러 · 평가원 9월 모평 10번',
          bossName: '🏹 외접원과 사인법칙의 성기사',
          scoreReward: 9,
          xpReward: 70,
          symbols: [
            { sym: '$\\dfrac{a}{\\sin A} = 2R$', desc: '삼각형의 한 변의 길이 $a$를 마주 보는 각의 사인값 $\\sin A$로 나누면 외접원의 지름 $2R$과 같다는 사인법칙' },
            { sym: '$c^2 = a^2 + b^2 - 2ab\\cos C$', desc: '두 변의 길이와 끼인각을 알 때 나머지 한 변의 길이를 구하는 코사인법칙' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 도형 직관] 반지름이 R일 때 지름의 길이',
              know: '원의 중심을 지나는 가장 긴 선분인 지름의 길이는 반지름 $R$의 $2$배인 $2R$입니다.',
              stem: '외접원의 반지름의 길이가 $R = 3$일 때, 외접원의 지름 $2R$의 길이는?',
              options: ['$3$', '$4$', '$5$', '$6$', '$9$'],
              answer: 4,
              exp: '지름은 반지름의 $2$배이므로 $2 \\times 3 = 6$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 사인법칙으로 변의 길이 구하기',
              know: '사인법칙 $\\dfrac{a}{\\sin A} = 2R$의 양변에 $\\sin A$를 곱하면 $a = 2R \\sin A$입니다.',
              stem: '외접원의 지름이 $2R = 6$이고 $\\sin A = \\dfrac{1}{2}$일 때, 마주 보는 변 $a = 2R\\sin A$의 길이는?',
              options: ['$1$', '$2$', '$3$', '$4$', '$6$'],
              answer: 3,
              exp: '$a = 6 \\times \\dfrac{1}{2} = 3$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [보스 격파] 코사인법칙과 외접원의 결합',
              know: '두 변 $a=3, b=3$이고 끼인각 $C$에 대하여 $\\cos C = -\\dfrac{1}{3}$일 때 코사인법칙을 적용합니다.',
              stem: '삼각형에서 $a=3, b=3, \\cos C = -\\dfrac{1}{3}$일 때, $c^2 = a^2 + b^2 - 2ab\\cos C$의 값은?',
              options: ['$12$', '$18$', '$20$', '$24$', '$27$'],
              answer: 4,
              exp: '$c^2 = 3^2 + 3^2 - 2 \\times 3 \\times 3 \\times \\left(-\\dfrac{1}{3}\\right) = 9 + 9 + 6 = 24$입니다.'
            }
          ]
        }
      ]
    },
    {
      id: 'w3',
      num: 3,
      icon: '⚡',
      name: '제3대륙 · 수학Ⅱ 극한·미분·적분 성채',
      sub: '함수의 연속 · 미분계수와 접선 · 삼차함수 극값 · 정적분 넓이 (목표: 45점 ➔ 74점)',
      targetScore: 74,
      emblemId: 'emblem_w3',
      emblemName: '⚡ 미적분학의 성배',
      shardYears: ['2026', '2025', '2024'],
      shardGrade: '고3',
      shardKeywords: ['함수의 극한', '연속', '미분계수', '도함수', '접선', '극대', '극소', '정적분', '넓이'],
      teacherAdvice: '공통과목 만점(74점)의 핵심 성채인 수학Ⅱ입니다! 할선이 접선으로 수렴하는 기하적 직관과 정적분 넓이 공식을 결합하면 모든 4점 문항이 열립니다.',
      min7014Links: [
        { title: '📈 할선이 접선으로 수렴하는 미분계수 기하 증명', url: 'https://min7014.github.io/math20190829002.html', type: 'Archive' },
        { title: '📐 구분구적법과 정적분 넓이 변환 (GeoGebra)', url: 'https://www.geogebra.org/u/min7014', type: 'GeoGebra' }
      ],
      stages: [
        {
          id: 'w3_s1',
          slug: 'csat26_02',
          url: 'board/csat26_02.html',
          gradeBadge: '2점 정찰병 · 2026학년도 수능 공통 2번',
          bossName: '⚡ 미분계수 순간변화율 파수꾼',
          scoreReward: 9,
          xpReward: 45,
          symbols: [
            { sym: '$(x^n)\\prime = n x^{n-1}$', desc: '지수 $n$이 앞으로 내려와 곱해지고 지수가 $1$ 줄어드는 다항함수 미분 약속' },
            { sym: '$\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h} = f\\prime(1)$', desc: '$x=1$에서의 순간변화율(접선의 기울기)을 뜻하는 미분계수 정의' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 곱셈 직관] 지수를 앞으로 내려 곱하기',
              know: '$(x^3)\\prime = 3x^2$이므로 앞에 $3$이 곱해진 $(3x^3)\\prime$은 $3 \\times 3x^2 = 9x^2$이고, $(4x)\\prime = 4$, 상수 $(1)\\prime = 0$입니다.',
              stem: '함수 $f(x) = 3x^3 + 4x + 1$을 미분한 도함수 $f\\prime(x) = [\\;\\text{(가)}\\;]$에 알맞은 식은?',
              options: ['$3x^2 + 4$', '$6x^2 + 4$', '$9x^2 + 4$', '$9x^2 + 1$', '$12x^2 + 4$'],
              answer: 3,
              exp: '$(3x^3)\\prime = 9x^2$, $(4x)\\prime = 4$, $(1)\\prime = 0$이므로 $f\\prime(x) = 9x^2 + 4$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 극한식을 미분계수 기호로 바꾸기',
              know: '미분계수의 정의에 의해 $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$는 도함수 $f\\prime(x)$에 $x=1$을 대입한 $f\\prime(1)$과 같습니다.',
              stem: '$\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$를 간단히 나타낸 기호는?',
              options: ['$f(0)$', '$f(1)$', '$f\\prime(0)$', '$f\\prime(1)$', '$f\\prime(2)$'],
              answer: 4,
              exp: '$x=1$에서의 미분계수 정의에 의해 $f\\prime(1)$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 2번 본문항 격파] $f\\prime(1)$의 값 계산하기',
              know: '도함수 $f\\prime(x) = 9x^2 + 4$에 $x=1$을 대입하면 $f\\prime(1) = 9(1)^2 + 4$입니다.',
              stem: '[2026학년도 수능 공통 2번] 함수 $f(x) = 3x^3 + 4x + 1$에 대하여 $\\lim_{h \\to 0} \\dfrac{f(1+h)-f(1)}{h}$의 값은? [2점]',
              options: ['$7$', '$9$', '$11$', '$13$', '$15$'],
              answer: 4,
              exp: '$f\\prime(1) = 9 + 4 = 13$이므로 정답은 4번($13$)입니다.'
            }
          ]
        },
        {
          id: 'w3_s2',
          slug: 'csat26_07',
          url: 'board/csat26_07.html',
          gradeBadge: '3점 정예 · 2026학년도 수능 공통 7번',
          bossName: '🌊 두 곡선 넓이의 정령',
          scoreReward: 10,
          xpReward: 60,
          symbols: [
            { sym: '$\\int_{a}^{b} \\{f(x)-g(x)\\}dx$', desc: '$x=a$부터 $x=b$까지 위쪽 곡선 $f(x)$에서 아래쪽 곡선 $g(x)$를 빼서 쌓은 넓이' },
            { sym: '$\\int x^2 dx = \\dfrac{1}{3}x^3 + C$', desc: '미분의 역연산으로 지수에 $1$을 더하고 그 수로 나누는 부정적분 공식' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 분수 덧셈] 위 식에서 아래 식 빼기',
              know: '두 곡선 $y = x^2 + 3$과 $y = -\\dfrac{1}{5}x^2 + 3$ 사이의 세로 길이는 위 식에서 아래 식을 뺀 값입니다.',
              stem: '$(x^2 + 3) - \\left(-\\dfrac{1}{5}x^2 + 3\\right) = [\\;\\text{(가)}\\;]$를 정리한 식은?',
              options: ['$\\dfrac{4}{5}x^2$', '$x^2$', '$\\dfrac{6}{5}x^2$', '$\\dfrac{6}{5}x^2 + 6$', '$2x^2$'],
              answer: 3,
              exp: '상수 $3 - 3 = 0$이 사라지고 $1 + \\dfrac{1}{5} = \\dfrac{6}{5}$이므로 $\\dfrac{6}{5}x^2$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [수식 빈칸 (나) 공략] 부정적분 구하기',
              know: '$\\int \\dfrac{6}{5}x^2 dx = \\dfrac{6}{5} \\times \\dfrac{1}{3}x^3 = \\dfrac{2}{5}x^3$입니다.',
              stem: '정적분 $\\int_{0}^{2} \\dfrac{6}{5}x^2 dx = \\left[\\;\\text{(나)}\\;\\right]_{0}^{2}$에서 빈칸 $(\\text{나})$에 알맞은 식은?',
              options: ['$\\dfrac{1}{5}x^3$', '$\\dfrac{2}{5}x^3$', '$\\dfrac{3}{5}x^3$', '$\\dfrac{6}{5}x^3$', '$\\dfrac{2}{3}x^3$'],
              answer: 2,
              exp: '$\\dfrac{6}{5} \\times \\dfrac{1}{3}x^3 = \\dfrac{2}{5}x^3$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 7번 본문항 격파] $x=0$부터 $x=2$까지 넓이 구하기',
              know: '$\\left[\\dfrac{2}{5}x^3\\right]_{0}^{2}$에 $x=2$를 대입하면 $\\dfrac{2}{5} \\times 2^3 = \\dfrac{2}{5} \\times 8$입니다.',
              stem: '[2026학년도 수능 공통 7번] 두 곡선 $y=x^2+3, y=-\\dfrac{1}{5}x^2+3$ 및 직선 $x=2$로 둘러싸인 부분의 넓이는? [3점]',
              options: ['$\\dfrac{12}{5}$', '$\\dfrac{14}{5}$', '$\\dfrac{16}{5}$', '$\\dfrac{18}{5}$', '$4$'],
              answer: 3,
              exp: '$\\dfrac{2}{5} \\times 8 = \\dfrac{16}{5}$이므로 정답은 3번($\\dfrac{16}{5}$)입니다.'
            }
          ]
        },
        {
          id: 'w3_s3',
          slug: 'c30915',
          url: 'board/c30915.html',
          gradeBadge: '4점 보스 · 평가원 9월 모평 15번',
          bossName: '🏰 정적분 함수 결정의 대마법사',
          scoreReward: 10,
          xpReward: 80,
          symbols: [
            { sym: '$\\int_{a}^{a} f(t)dt = 0$', desc: '정적분의 시작점(아래끝)과 끝점(위끝)이 같으면 넓이가 $0$이라는 약속' },
            { sym: '$\\dfrac{d}{dx}\\int_{a}^{x} f(t)dt = f(x)$', desc: '정적분으로 정의된 함수를 $x$로 미분하면 안의 함수 $f(x)$가 그대로 나오는 미적분학의 기본정리' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 직관] 시작과 끝이 같을 때의 정적분 값',
              know: '수직선에서 $x=1$에서 출발해 $x=1$에서 멈추면 움직인 폭이 $0$이므로 $\\int_{1}^{1} f(t)dt = 0$입니다.',
              stem: '임의의 연속함수 $f(t)$에 대하여 $\\int_{1}^{1} f(t)dt$의 값은 항상 얼마인가요?',
              options: ['$-1$', '$0$', '$1$', '$2$', '$f(1)$'],
              answer: 2,
              exp: '위끝과 아래끝이 같으면 정적분의 값은 항상 $0$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 정적분 함수 양변 미분하기',
              know: '$g(x) = \\int_{1}^{x} (t^2 - 4)dt$의 양변을 $x$에 대하여 미분하면 $t$가 $x$로 바뀌어 $g\\prime(x) = x^2 - 4$가 됩니다.',
              stem: '$g(x) = \\int_{1}^{x} (t^2 - 4)dt$일 때, 도함수 $g\\prime(x)$가 $0$이 되는 양수 $x$의 값은?',
              options: ['$1$', '$2$', '$3$', '$4$', '$5$'],
              answer: 2,
              exp: '$g\\prime(x) = x^2 - 4 = (x-2)(x+2) = 0$에서 양수 $x = 2$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [보스 격파] 극솟값 $g(2)$ 구하기',
              know: '$g(2) = \\int_{1}^{2} (t^2 - 4)dt = \\left[\\dfrac{1}{3}t^3 - 4t\\right]_{1}^{2}$를 계산합니다.',
              stem: '위 함수 $g(x) = \\int_{1}^{x}(t^2-4)dt$에 대하여 $x=1$일 때의 함숫값 $g(1)$과 도함수 $g\\prime(2)$의 합 $g(1)+g\\prime(2)$는?',
              options: ['$-2$', '$-1$', '$0$', '$1$', '$2$'],
              answer: 3,
              exp: '$g(1)=0$이고 $g\\prime(2)=2^2-4=0$이므로 $g(1)+g\\prime(2) = 0$입니다.'
            }
          ]
        }
      ]
    },
    {
      id: 'w4',
      num: 4,
      icon: '🧭',
      name: '제4대륙 · 선택과목 3대 신전 (미적분 · 확통 · 기하)',
      sub: '삼각극한과 치환적분 · 조건부확률과 정규분포 · 이차곡선과 공간도형 (목표: 74점 ➔ 88점)',
      targetScore: 88,
      emblemId: 'emblem_w4',
      emblemName: '🧭 선택과목 신전의 열쇠',
      shardYears: ['2026', '2025', '2024'],
      shardGrade: '고3',
      shardKeywords: ['삼각함수의 극한', '치환적분', '급수', '조건부확률', '독립시행', '정규분포', '포물선', '타원', '쌍곡선', '정사영'],
      teacherAdvice: '선택과목 8문항(26점) 중 23~28번을 완벽히 잡으면 88점(안정 1등급권)에 진입합니다! 미적분·확통·기하 3대 신전을 차례대로 탐험해 보세요.',
      min7014Links: [
        { title: '📐 lim(sin θ / θ)=1 부채꼴 넓이 비교 시각적 증명 (PDF)', url: 'https://min7014.github.io/2016032701.pdf', type: 'PDF' },
        { title: '🔮 단델린의 구(Dandelin Spheres)와 원뿔곡선 초점 증명', url: 'https://min7014.github.io/math20190810126.html', type: 'Archive' }
      ],
      stages: [
        {
          id: 'w4_s1',
          slug: 'csat26_m23',
          url: 'board/csat26_m23.html',
          gradeBadge: '미적분 신전 · 2026 수능 미적분 23번',
          bossName: '🌀 삼각함수 극한의 수호신',
          scoreReward: 5,
          xpReward: 50,
          symbols: [
            { sym: '$\\lim_{x \\to 0} \\dfrac{\\sin x}{x} = 1,\\; \\lim_{x \\to 0} \\dfrac{\\tan x}{x} = 1$', desc: '각 $x$(라디안)가 $0$에 한없이 가까워질 때 $\\sin x, \\tan x$는 $x$와 비율이 $1:1$로 같아진다는 극한 공식' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 분수 나눗셈] 계수 비율 찾기',
              know: '$\\lim_{x \\to 0} \\dfrac{\\sin(ax)}{bx} = \\dfrac{a}{b}$처럼, $x \\to 0$일 때는 $x$ 앞의 숫자 비율로 극한값이 결정됩니다.',
              stem: '초등학교 분수 나눗셈에서 $6 \\div 2 = \\dfrac{6}{2}$를 약분한 값은?',
              options: ['$1$', '$2$', '$3$', '$4$', '$6$'],
              answer: 3,
              exp: '$6 \\div 2 = 3$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 삼각함수 기본 극한 적용',
              know: '$\\lim_{x \\to 0} \\dfrac{\\sin 3x}{x} = 3 \\lim_{x \\to 0} \\dfrac{\\sin 3x}{3x} = 3 \\times 1 = 3$입니다.',
              stem: '$\\lim_{x \\to 0} \\dfrac{\\tan 6x}{2x}$의 극한값은?',
              options: ['$1$', '$2$', '$3$', '$4$', '$6$'],
              answer: 3,
              exp: '$\\dfrac{6}{2} \\times 1 = 3$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 미적 23번 격파] 삼각함수 극한 완성',
              know: '분자와 분모를 $x$로 나누어 각각의 극한값을 구합니다.',
              stem: '$\\lim_{x \\to 0} \\dfrac{\\sin 4x + \\tan 2x}{2x}$를 계산한 값은?',
              options: ['$1$', '$2$', '$3$', '$4$', '$5$'],
              answer: 3,
              exp: '$\\lim_{x \\to 0}\\left(\\dfrac{\\sin 4x}{2x} + \\dfrac{\\tan 2x}{2x}\\right) = 2 + 1 = 3$입니다.'
            }
          ]
        },
        {
          id: 'w4_s2',
          slug: '1b623c24',
          url: 'board/1b623c24.html',
          gradeBadge: '확통 신전 · 평가원 모평 확통 28번',
          bossName: '🎲 독립시행과 조건부확률의 예언자',
          scoreReward: 5,
          xpReward: 65,
          symbols: [
            { sym: '$P(B|A) = \\dfrac{P(A \\cap B)}{P(A)}$', desc: '사건 $A$가 일어났을 때 그중에서 사건 $B$도 함께 일어날 조건부확률 약속' },
            { sym: '$_n\\mathrm{C}_r p^r (1-p)^{n-r}$', desc: '$n$번 반복 시행에서 원하는 사건이 정확히 $r$번 일어날 독립시행의 확률' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 홀짝 직관] 카드를 짝수 번 뒤집기',
              know: '앞면이 보이던 카드를 $1$번 뒤집으면 뒷면, $2$번(짝수 번) 뒤집으면 다시 처음과 같은 앞면이 됩니다.',
              stem: '앞면으로 놓인 카드를 총 $2$번 뒤집었을 때, 마지막에 보이는 면은 무엇인가요?',
              options: ['앞면', '뒷면', '옆면', '알 수 없다', '사라진다'],
              answer: 1,
              exp: '앞면 ➔ 뒷면(1회) ➔ 앞면(2회)이므로 짝수 번 뒤집으면 다시 앞면이 됩니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 주사위에서 짝수의 눈이 나올 확률',
              know: '$1$부터 $6$까지의 주사위 눈 중 짝수는 $2, 4, 6$의 $3$개이므로 확률은 $\\dfrac{3}{6} = \\dfrac{1}{2}$입니다.',
              stem: '한 개의 주사위를 $2$번 던질 때, 두 번 모두 짝수의 눈이 나올 확률은?',
              options: ['$\\dfrac{1}{8}$', '$\\dfrac{1}{6}$', '$\\dfrac{1}{4}$', '$\\dfrac{1}{3}$', '$\\dfrac{1}{2}$'],
              answer: 3,
              exp: '$\\dfrac{1}{2} \\times \\dfrac{1}{2} = \\dfrac{1}{4}$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [확통 신전 격파] 조건부확률 분수 계산',
              know: '전체 사건 $A$의 확률이 $P(A) = \\dfrac{5}{16}$이고 교집합 $P(A \\cap B) = \\dfrac{3}{16}$일 때 조건부확률은 $\\dfrac{P(A \\cap B)}{P(A)}$입니다.',
              stem: '$P(A) = \\dfrac{5}{16},\\; P(A \\cap B) = \\dfrac{3}{16}$일 때 조건부확률 $P(B|A) = \\dfrac{P(A \\cap B)}{P(A)}$의 값은?',
              options: ['$\\dfrac{1}{5}$', '$\\dfrac{2}{5}$', '$\\dfrac{3}{5}$', '$\\dfrac{4}{5}$', '$\\dfrac{3}{8}$'],
              answer: 3,
              exp: '분모 $16$을 약분하면 $\\dfrac{3}{5}$입니다.'
            }
          ]
        },
        {
          id: 'w4_s3',
          slug: 'csat26_g29',
          url: 'board/csat26_g29.html',
          gradeBadge: '기하 신전 · 2026 수능 기하 29번',
          bossName: '🪐 포물선과 타원 초점의 지배자',
          scoreReward: 4,
          xpReward: 70,
          symbols: [
            { sym: '$\\overline{PF} + \\overline{PF\\prime} = 2a$', desc: '타원 위의 임의의 점 $P$에서 두 초점 $F, F\\prime$까지의 거리의 합은 장축의 길이 $2a$로 항상 일정하다는 정의' },
            { sym: '$\\overline{PF} = \\overline{PH}$', desc: '포물선 위의 점 $P$에서 초점 $F$까지의 거리와 준선까지의 수직 거리 $\\overline{PH}$는 항상 같다는 정의' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 덧셈 직관] 실의 길이(장축의 길이) 구하기',
              know: '타원의 장축의 길이가 $2a = 10$일 때, 타원 위의 점 $P$에서 두 초점까지의 거리의 합 $\\overline{PF}+\\overline{PF\\prime}$은 항상 $10$입니다.',
              stem: '장축의 길이가 $10$인 타원에서 한 초점까지의 거리가 $\\overline{PF} = 3$일 때, 다른 초점까지의 거리 $\\overline{PF\\prime}$은?',
              options: ['$4$', '$5$', '$6$', '$7$', '$8$'],
              answer: 4,
              exp: '$\\overline{PF} + \\overline{PF\\prime} = 10$이므로 $\\overline{PF\\prime} = 10 - 3 = 7$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 포물선 초점과 준선 거리 등치',
              know: '포물선 $y^2 = 4px$에서 초점은 $F(p, 0)$, 준선은 $x = -p$이며, 포물선 위의 점에서 초점까지 거리와 준선까지 거리는 같습니다.',
              stem: '포물선 $y^2 = 8x$ ($4p=8 \\implies p=2$)의 초점 $F(2, 0)$과 준선 $x = -2$ 사이의 거리는?',
              options: ['$2$', '$3$', '$4$', '$6$', '$8$'],
              answer: 3,
              exp: '$x=2$에서 $x=-2$까지의 거리는 $2 - (-2) = 4$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [기하 신전 격파] 타원의 초점 공식 $c^2 = a^2 - b^2$',
              know: '타원 $\\dfrac{x^2}{a^2} + \\dfrac{y^2}{b^2} = 1$ ($a>b>0$)의 초점 좌표 $(c, 0)$은 $c^2 = a^2 - b^2$을 만족합니다.',
              stem: '타원 $\\dfrac{x^2}{25} + \\dfrac{y^2}{9} = 1$의 양의 초점 $F(c, 0)$에서 $c$의 값은?',
              options: ['$2$', '$3$', '$4$', '$5$', '$6$'],
              answer: 3,
              exp: '$c^2 = 25 - 9 = 16$이므로 $c = 4$입니다.'
            }
          ]
        }
      ]
    },
    {
      id: 'w5',
      num: 5,
      icon: '🐉',
      name: '제5대륙 · 4점 준킬러·킬러 보스 레이드',
      sub: '공통 21·22번 & 선택 29·30번 최고난도 보스 격파 (목표: 88점 ➔ 96점)',
      targetScore: 96,
      emblemId: 'emblem_w5',
      emblemName: '🐉 킬러 정복자의 검',
      shardYears: ['2026', '2025', '2024'],
      shardGrade: '고3',
      shardKeywords: ['역함수', '귀납적 정의', '미분가능', '합성함수', '정적분으로 정의된 함수', '벡터의 내적'],
      teacherAdvice: '수능 수학 1등급과 100점 만점을 가르는 22번·30번 킬러 보스 대륙입니다! 초등 눈높이 디딤돌 보호막으로 보스의 수식 장갑을 한 겹씩 벗겨내면 누구나 격파할 수 있습니다!',
      min7014Links: [
        { title: '👑 지수·로그 역함수 대칭과 기울기 기하 분석', url: 'https://min7014.github.io/', type: 'Archive' },
        { title: '🧭 평면벡터 내적과 정사영 최대·최소 시뮬레이션', url: 'https://www.geogebra.org/u/min7014', type: 'GeoGebra' }
      ],
      stages: [
        {
          id: 'w5_s1',
          slug: 'csat26_22',
          url: 'board/csat26_22.html',
          gradeBadge: '4점 대보스 · 2026학년도 수능 공통 22번',
          bossName: '🐉 [공통 22번 대보스] 지수·로그 역함수 대칭의 군주',
          scoreReward: 4,
          xpReward: 120,
          symbols: [
            { sym: '$y = x$ 대칭 $\\iff (a, b) \\leftrightarrow (b, a)$', desc: '지수함수와 로그함수가 역함수 관계일 때 두 교점의 $x$좌표와 $y$좌표가 서로 뒤바뀌는 대칭 성질' },
            { sym: '기울기 $m = \\dfrac{y_2-y_1}{x_2-x_1}$', desc: '두 점 사이의 세로 변화량($\\Delta y$)을 가로 변화량($\\Delta x$)으로 나눈 직선의 기울기' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 직관 타격] 직선 y=x 대칭점 찾기',
              know: '좌표평면에서 점 $(a, b)$를 직선 $y = x$에 대하여 대칭이동하면 $x$좌표와 $y$좌표의 자리가 바뀌어 $(b, a)$가 됩니다.',
              stem: '점 $A(2, 5)$를 직선 $y = x$에 대하여 대칭이동한 점 $B$의 좌표는?',
              options: ['$(2, -5)$', '$(-2, 5)$', '$(5, 2)$', '$(-5, -2)$', '$(5, 5)$'],
              answer: 3,
              exp: '$x$좌표와 $y$좌표의 자리를 바꾸면 $(5, 2)$가 됩니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 기울기가 -1인 직선 위의 두 점 관계',
              know: '기울기가 $-1$인 직선 $y = -x + k$ 위의 두 점 $(x_1, y_1), (x_2, y_2)$에서는 항상 $x_1 + y_1 = x_2 + y_2 = k$가 성립합니다.',
              stem: '두 점 $A(a, b)$와 $B(c, d)$를 지나는 직선의 기울기가 $-1$이고 $c - a = 4$일 때, $b - d$의 값은?',
              options: ['$1$', '$2$', '$3$', '$4$', '$5$'],
              answer: 4,
              exp: '기울기 $\\dfrac{d-b}{c-a} = -1 \\implies b - d = c - a = 4$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [22번 대보스 격파] 직각이등변삼각형 빗변 길이와 대칭 결합',
              know: '기울기가 $-1$인 직선 위에서 $\\Delta x = k, \\Delta y = -k$이면 두 점 사이의 거리(빗변)는 $\\sqrt{k^2 + k^2} = \\sqrt{2}k$입니다.',
              stem: '기울기가 $-1$인 직선 위의 두 점 $A, B$ 사이의 거리가 $\\overline{AB} = 3\\sqrt{2}$일 때, 두 점의 $x$좌표의 차 $|x_B - x_A|$는?',
              options: ['$1$', '$2$', '$3$', '$4$', '$6$'],
              answer: 3,
              exp: '$\\sqrt{2}|x_B - x_A| = 3\\sqrt{2}$이므로 양변을 $\\sqrt{2}$로 나누면 $|x_B - x_A| = 3$입니다. (더 깊은 풀이는 [🔎 풀스크린 22번 디딤돌]에서 완성하세요!)'
            }
          ]
        },
        {
          id: 'w5_s2',
          slug: 'csat26_m30',
          url: 'board/csat26_m30.html',
          gradeBadge: '4점 최종보스 · 2026학년도 수능 미적분 30번',
          bossName: '👑 [미적 30번 최종보스] 역함수 미분법의 제왕',
          scoreReward: 4,
          xpReward: 120,
          symbols: [
            { sym: '$g(f(x)) = x \\implies g\\prime(f(x)) f\\prime(x) = 1$', desc: '원래 함수의 접선 기울기 $f\\prime(x)$와 역함수의 대응점 접선 기울기 $g\\prime(f(x))$를 곱하면 항상 $1$(역수 관계)이 된다는 역함수 미분법' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 역수 직관] 곱해서 1이 되는 수 찾기',
              know: '두 수를 곱해서 $1$이 될 때 한 수를 다른 수의 역수라고 부릅니다. 예를 들어 $4 \\times \\dfrac{1}{4} = 1$입니다.',
              stem: '$f\\prime(a) = 5$일 때, $f\\prime(a) \\times g\\prime(b) = 1$을 만족하는 역함수의 미분계수 $g\\prime(b)$의 값은?',
              options: ['$\\dfrac{1}{5}$', '$\\dfrac{2}{5}$', '$\\dfrac{1}{2}$', '$1$', '$5$'],
              answer: 1,
              exp: '$5$와 곱해서 $1$이 되는 역수는 $\\dfrac{1}{5}$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 역함수 함숫값 대응 찾기',
              know: '$f(x)$의 역함수가 $g(x)$일 때, $g(b) = a \\iff f(a) = b$입니다.',
              stem: '증가하는 미분가능한 함수 $f(x) = x^3 + 2x + 1$의 역함수를 $g(x)$라 할 때, $f(1) = 4$이면 $g(4)$의 값은?',
              options: ['$0$', '$1$', '$2$', '$3$', '$4$'],
              answer: 2,
              exp: '$f(1) = 4$이므로 역함수 정의에 의해 $g(4) = 1$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [미적 30번 최종보스 격파] 역함수 미분계수 $g\\prime(4)$ 도출',
              know: '$f(x) = x^3 + 2x + 1$에서 $f(1) = 4$이고 $f\\prime(x) = 3x^2 + 2$이므로 $f\\prime(1) = 5$입니다.',
              stem: '위 함수 $f(x) = x^3 + 2x + 1$의 역함수 $g(x)$에 대하여 $g\\prime(4) = \\dfrac{1}{f\\prime(1)}$의 값은?',
              options: ['$\\dfrac{1}{7}$', '$\\dfrac{1}{6}$', '$\\dfrac{1}{5}$', '$\\dfrac{1}{4}$', '$\\dfrac{1}{3}$'],
              answer: 3,
              exp: '$g(4)=1$이고 $f\\prime(1)=3(1)^2+2=5$이므로 $g\\prime(4) = \\dfrac{1}{f\\prime(1)} = \\dfrac{1}{5}$입니다.'
            }
          ]
        }
      ]
    },
    {
      id: 'w6',
      num: 6,
      icon: '👑',
      name: '제6대륙 · 실전 수능 100점 만점 마스터리 전당',
      sub: '2006~2026 전 연도 16,548문항 무제한 실전 레이드 & 약점 완전 정복 (목표: 96점 ➔ 100점 만점)',
      targetScore: 100,
      emblemId: 'emblem_w6',
      emblemName: '👑 수능 수학 100점 만점의 왕관',
      shardYears: ['2026', '2025', '2024', '2023', '2022', '2021', '2020'],
      shardGrade: '고3',
      shardKeywords: ['수능', '모의평가', '미적분', '확률과 통계', '기하'],
      teacherAdvice: '축하합니다! 이제 마지막 100점 만점의 왕관을 쓸 차례입니다. 16,548문항 전체 기출 아카이브에서 실시간으로 문제를 소환하거나 최종 마스터리 시련을 완수해 수능 수학 100점 만점을 달성하세요!',
      min7014Links: [
        { title: '🏛️ 민은기 선생님의 수학자료실 전체 3,400+ 주제 총람', url: 'https://min7014.github.io/', type: 'Archive' },
        { title: '📺 유튜브 수학 개념·기하 시각적 증명 채널 (@min7014)', url: 'https://www.youtube.com/@min7014', type: 'YouTube' }
      ],
      stages: [
        {
          id: 'w6_s1',
          slug: 'csat26_g30',
          url: 'board/csat26_g30.html',
          gradeBadge: '100점 만점 최종 관문 · 2026 수능 기하 30번',
          bossName: '👑 [수능 100점 수호신] 평면벡터 내적과 단델린 구의 지배자',
          scoreReward: 4,
          xpReward: 150,
          symbols: [
            { sym: '$\\vec{a} \\cdot \\vec{b} = |\\vec{a}||\\vec{b}|\\cos\\theta$', desc: '한 벡터를 다른 벡터 위로 수직으로 비춘 그림자(정사영) 길이와 원래 길이를 곱하는 내적의 기하적 의미' },
            { sym: '$\\vec{AP} = \\vec{AO} + \\vec{OP}$', desc: '원 위의 움직이는 점 $P$로 가는 벡터를 고정된 중심 $O$를 거쳐 분해하는 핵심 전략' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🔰 1단계 · [초등 각도 직관] 두 화살표가 같은 방향일 때 최댓값',
              know: '두 벡터가 똑같은 방향($\\theta = 0^\\circ, \\cos 0^\\circ = 1$)을 가리킬 때 내적은 가장 커지고, 정반대 방향($\\theta = 180^\\circ, \\cos 180^\\circ = -1$)일 때 가장 작아집니다.',
              stem: '길이가 $3$인 벡터 $\\vec{a}$와 길이가 $2$인 벡터 $\\vec{b}$가 같은 방향을 향할 때, 내적 $\\vec{a}\\cdot\\vec{b}$의 최댓값은?',
              options: ['$1$', '$3$', '$5$', '$6$', '$9$'],
              answer: 4,
              exp: '같은 방향일 때 $\\cos 0^\\circ = 1$이므로 최댓값은 $3 \\times 2 \\times 1 = 6$입니다.'
            },
            {
              stepNum: 2,
              label: '🌱 2단계 · [기호 번역 브릿지] 원의 중심을 거쳐 벡터 분해하기',
              know: '중심이 $O$이고 반지름이 $r=2$인 원 위의 점 $P$에 대하여 $|\\vec{AO}|=5$이면 $|\\vec{AP}| = |\\vec{AO}+\\vec{OP}|$의 최댓값은 $5+2=7$, 최솟값은 $5-2=3$입니다.',
              stem: '원의 중심 $O$까지의 거리가 $|\\vec{AO}|=5$이고 원의 반지름이 $2$일 때, $|\\vec{AP}|$의 최댓값 $M$과 최솟값 $m$의 합 $M+m$은?',
              options: ['$6$', '$8$', '$10$', '$12$', '$14$'],
              answer: 3,
              exp: '$M = 5+2 = 7$, $m = 5-2 = 3$이므로 $M + m = 10$입니다.'
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [수능 100점 만점 달성!] 수능 배점 총합 완성 확인',
              know: '수능 수학 영역은 2점 3문항(6점) + 3점 14문항(42점) + 4점 13문항(52점)으로 구성되어 모든 문항을 디딤돌 원리로 정복하면 총점 100점 만점이 됩니다.',
              stem: '수능 수학 영역에서 2점 3문항($6$점), 3점 14문항($42$점), 4점 13문항($52$점)을 모두 맞혔을 때 달성하는 최종 점수는?',
              options: ['$88$점', '$92$점', '$96$점', '$98$점', '$100$점 만점'],
              answer: 5,
              exp: '$6 + 42 + 52 = 100$점 만점! 축하합니다, 수능 수학 100점 만점의 왕관을 획득하셨습니다!'
            }
          ]
        }
      ]
    }
  ];

  // 🚀 [60초 3D 스피드 디딤돌 블리츠] mathteacher 엄선 수능 필수 공식·직관 15문항
  var SPEED_BLITZ_QUESTIONS = [
    { unit: '고1 공통 · 원과 직선', stem: '원의 중심에서 직선까지의 거리가 $d=4$, 반지름이 $r=4$일 때 원과 직선의 교점의 개수는?', options: ['$0$개', '$1$개 (접한다)', '$2$개', '$3$개', '$4$개'], answer: 2, hint: '$d = r$이면 원과 직선은 한 점에서 접합니다.' },
    { unit: '고1 공통 · 이차함수 대칭축', stem: '이차함수 $y = (x-1)(x-7)$의 그래프의 대칭축의 방정식은?', options: ['$x=2$', '$x=3$', '$x=4$', '$x=5$', '$x=6$'], answer: 3, hint: '두 절편 $1$과 $7$의 중점 $\\dfrac{1+7}{2}=4$가 대칭축입니다.' },
    { unit: '수학Ⅰ · 지수법칙', stem: '$2^3 \\times 2^{-1}$의 값은?', options: ['$1$', '$2$', '$4$', '$8$', '$16$'], answer: 3, hint: '$2^{3+(-1)} = 2^2 = 4$입니다.' },
    { unit: '수학Ⅰ · 로그의 정의', stem: '$\\log_3 9 + \\log_3 1$의 값은?', options: ['$0$', '$1$', '$2$', '$3$', '$9$'], answer: 3, hint: '$\\log_3 3^2 = 2$이고 $\\log_3 1 = 0$이므로 $2+0=2$입니다.' },
    { unit: '수학Ⅰ · 삼각함수 특수각', stem: '$2\\sin\\dfrac{\\pi}{6} + \\cos 0$의 값은?', options: ['$1$', '$\\dfrac{3}{2}$', '$2$', '$\\dfrac{5}{2}$', '$3$'], answer: 3, hint: '$\\sin\\dfrac{\\pi}{6}=\\dfrac{1}{2},\\; \\cos 0 = 1$이므로 $1 + 1 = 2$입니다.' },
    { unit: '수학Ⅰ · 사인법칙', stem: '외접원의 반지름이 $R=5$인 삼각형 $\\mathrm{ABC}$에서 $\\dfrac{a}{\\sin A}$의 값은?', options: ['$5$', '$8$', '$10$', '$15$', '$20$'], answer: 3, hint: '사인법칙 $\\dfrac{a}{\\sin A} = 2R = 10$입니다.' },
    { unit: '수학Ⅰ · 등차수열 중항', stem: '세 수 $2, x, 10$이 이 순서대로 등차수열을 이룰 때 $x$의 값은?', options: ['$4$', '$5$', '$6$', '$7$', '$8$'], answer: 3, hint: '등차중항 $x = \\dfrac{2+10}{2} = 6$입니다.' },
    { unit: '수학Ⅰ · 시그마의 합', stem: '$\\sum_{k=1}^{5} k = 1+2+3+4+5$의 값은?', options: ['$10$', '$12$', '$15$', '$20$', '$25$'], answer: 3, hint: '$\\dfrac{5 \\times 6}{2} = 15$입니다.' },
    { unit: '수학Ⅱ · 다항함수 미분계수', stem: '함수 $f(x) = x^3 + 2x$에 대하여 $f\\prime(1)$의 값은?', options: ['$3$', '$4$', '$5$', '$6$', '$7$'], answer: 3, hint: '$f\\prime(x) = 3x^2 + 2$이므로 $f\\prime(1) = 3 + 2 = 5$입니다.' },
    { unit: '수학Ⅱ · 정적분 기본성질', stem: '임의의 다항함수 $f(x)$에 대하여 정적분 $\\int_{2}^{2} f(x)dx$의 값은?', options: ['$-2$', '$-1$', '$0$', '$1$', '$2$'], answer: 3, hint: '위끝과 아래끝이 같으면 정적분의 값은 항상 $0$입니다.' },
    { unit: '수학Ⅱ · 이차곡선 정적분 넓이', stem: '포물선 $y = x^2 - 2x$와 $x$축으로 둘러싸인 부분의 넓이 $\\dfrac{|a|(\\beta-\\alpha)^3}{6}$는?', options: ['$\\dfrac{2}{3}$', '$1$', '$\\dfrac{4}{3}$', '$\\dfrac{5}{3}$', '$2$'], answer: 3, hint: '두 근이 $0, 2$이므로 넓이 공식 $\\dfrac{1 \\times (2-0)^3}{6} = \\dfrac{8}{6} = \\dfrac{4}{3}$입니다.' },
    { unit: '미적분 · 삼각함수의 극한', stem: '$\\lim_{x \\to 0} \\dfrac{\\sin 5x}{x}$의 값은?', options: ['$1$', '$3$', '$5$', '$7$', '$10$'], answer: 3, hint: '$\\lim_{x \\to 0} 5 \\cdot \\dfrac{\\sin 5x}{5x} = 5$입니다.' },
    { unit: '미적분 · 자연상수 e와 미분', stem: '함수 $f(x) = e^{2x}$를 미분한 도함수 $f\\prime(x)$에 대하여 $f\\prime(0)$의 값은?', options: ['$0$', '$1$', '$2$', '$e$', '$2e$'], answer: 3, hint: '$f\\prime(x) = 2e^{2x}$이므로 $f\\prime(0) = 2e^0 = 2$입니다.' },
    { unit: '확통 · 조건부확률', stem: '$P(A) = \\dfrac{1}{2},\\; P(A \\cap B) = \\dfrac{1}{6}$일 때 조건부확률 $P(B|A)$의 값은?', options: ['$\\dfrac{1}{6}$', '$\\dfrac{1}{4}$', '$\\dfrac{1}{3}$', '$\\dfrac{1}{2}$', '$\\dfrac{2}{3}$'], answer: 3, hint: '$P(B|A) = \\dfrac{P(A \\cap B)}{P(A)} = \\dfrac{1/6}{1/2} = \\dfrac{1}{3}$입니다.' },
    { unit: '기하 · 평면벡터 내적 최댓값', stem: '길이가 $|\vec{a}|=4, |\vec{b}|=3$인 두 벡터가 같은 방향($\\theta=0^\\circ$)을 향할 때 $\\vec{a}\\cdot\\vec{b}$의 값은?', options: ['$7$', '$9$', '$12$', '$15$', '$16$'], answer: 3, hint: '같은 방향이면 $\\cos 0^\\circ = 1$이므로 $4 \\times 3 \\times 1 = 12$입니다.' }
  ];

  // 🃏 [로그라이크 수학자의 성물 10종: Relics of the Mathematicians] (Slay the Spire / Hades / Balatro 벤치마킹)
  var MATH_RELICS = [
    {
      id: 'relic_dandelin',
      icon: '🔮',
      name: '단델린의 황금 쌍구',
      rarity: 'SSR',
      formula: '$\\overline{PF}+\\overline{PF\\prime}=2a$',
      intuition: '원뿔 안에 내접하는 두 구의 접점이 이차곡선의 초점이 된다는 기하학적 불변량 원리',
      effectDesc: '3D 보조선 상시 활성화 + 비급서·필살기 게이지 충전량 +50% 가속'
    },
    {
      id: 'relic_gauss',
      icon: '📐',
      name: '가우스의 대칭 덧셈 저울',
      rarity: 'SR',
      formula: '$S_n = \\dfrac{n(a_1+a_n)}{2}$',
      intuition: '양 끝에서 대칭인 두 항의 합이 항상 일정하다는 등차수열 대칭 직관',
      effectDesc: '1단계 정답 시 보너스 XP +50% & 전투 시작 시 +1 콤보 선충전'
    },
    {
      id: 'relic_euler',
      icon: '🌀',
      name: '오일러의 초월 나선 나침반',
      rarity: 'SSR',
      formula: '$e^{i\\theta}=\\cos\\theta+i\\sin\\theta$',
      intuition: '지수함수의 성장이 복소평면 단위원 회전과 하나로 통합되는 초월 항등식',
      effectDesc: '오답 발생 시 콤보 깨짐 1회 완벽 방어 + 3D 결계 회전 감속'
    },
    {
      id: 'relic_fermat',
      icon: '⛰️',
      name: '페르마의 극치 프리즘',
      rarity: 'SR',
      formula: '$f\\prime(c)=0$',
      intuition: '미분가능한 함수가 극대·극소를 갖는 봉우리와 골짜기에서 접선은 수평이 된다는 정리',
      effectDesc: '2단계 수식 빈칸 (가)·(나) 정답 시 치명타 발동 (+25 XP 추가)'
    },
    {
      id: 'relic_leibniz',
      icon: '📜',
      name: '라이프니츠의 미적분 태엽',
      rarity: 'SSR',
      formula: '$\\int_a^b f(x)dx = F(b)-F(a)$',
      intuition: '무수히 잘게 쪼갠 넓이의 합(정적분)을 부정적분의 양 끝값 차이로 단번에 계산하는 마법',
      effectDesc: '보스 승리 시 총 XP 1.3배 증폭 & 수능 점수 +1점 추가 획득'
    },
    {
      id: 'relic_descartes',
      icon: '🪞',
      name: '데카르트의 y=x 대칭 거울',
      rarity: 'SR',
      formula: '$y=f(x) \\iff x=f^{-1}(y)$',
      intuition: '기하학적 도형을 좌표평면의 대수 방정식으로 번역하고 역함수 대칭을 비추는 거울',
      effectDesc: '전투 진입 시 5지선다 중 오답 함정 선지 1개를 자동 투시하여 표시'
    },
    {
      id: 'relic_pascal',
      icon: '🔺',
      name: '파스칼의 이항 삼각 성배',
      rarity: 'R',
      formula: '$_n\\mathrm{C}_r = {}_{n-1}\\mathrm{C}_{r-1}+{}_{n-1}\\mathrm{C}_r$',
      intuition: '이웃한 두 경우의 수를 더하면 다음 단계의 경우의 수가 탄생하는 조합의 연쇄 법칙',
      effectDesc: '3콤보 대신 2콤보부터 즉시 🔥 FEVER RUSH 조기 발동'
    },
    {
      id: 'relic_bernoulli',
      icon: '🎲',
      name: '베르누이의 독립시행 주사위',
      rarity: 'R',
      formula: '$P(X=r)={}_n\\mathrm{C}_r p^r(1-p)^{n-r}$',
      intuition: '반복되는 도전 속에서도 확률 법칙에 따라 반드시 목표에 수렴하는 불굴의 주사위',
      effectDesc: '보스 전투 승리 시 수능 점수 +2점 추가 보너스'
    },
    {
      id: 'relic_cauchy',
      icon: '⚡',
      name: '코시-슈바르츠의 정사영 창',
      rarity: 'SSR',
      formula: '$\\vec{a}\\cdot\\vec{b}=|\\vec{a}||\\vec{b}|\\cos\\theta$',
      intuition: '두 벡터가 완전히 같은 방향을 가리킬 때 내적 에너지가 최대가 된다는 코사인 정사영 원리',
      effectDesc: '1단계 정답 시 보스 외곽 방어력 50% 즉시 관통 파쇄 (+필살기 +20%)'
    },
    {
      id: 'relic_archimedes',
      icon: '⏳',
      name: '아르키메데스의 사색 모래시계',
      rarity: 'SSR',
      formula: '$V_{\\text{구}} : V_{\\text{원기둥}} = 2 : 3$',
      intuition: '"내 원을 밟지 마라!" 깊은 사색 속에서 모든 기하학적 난제는 풀린다는 유레카(Eureka)의 원리',
      effectDesc: '🧠 사색 통찰 게이지 충전 속도 2배 가속 & DEEP EUREKA!! 달성 시 수능 점수 +2점 추가 상승'
    }
  ];

  // 🌌 [4대 수학 성좌 각성 스킬트리: Constellations of Mastery] (Genshin Impact / Zelda 벤치마킹)
  var MATH_CONSTELLATIONS = [
    {
      id: 'const_archimedes',
      code: '♈ 제1성좌',
      name: '아르키메데스 대수·수열 성좌',
      color: '#fb923c',
      stars: [
        { id: 'c1_s1', star: '★1', name: '거듭제곱과 밑 통일의 별', formula: '$a^m \\times a^n = a^{m+n}$', buff: '지수·로그 1단계 돌파 시 보호막 +10% 추가 회복' },
        { id: 'c1_s2', star: '★★2', name: '시그마 소거의 별', formula: '$\\sum_{k=1}^n (a_{k+1}-a_k)=a_{n+1}-a_1$', buff: '모든 단계 정답 시 기본 XP +5 영구 증가' },
        { id: 'c1_s3', star: '★★★3', name: '귀납적 역추적의 태초성', formula: '$a_{n+1}=f(a_n) \\implies a_1$ 역추적', buff: '보스 클리어 시 수능 점수 +1점 영구 추가' }
      ]
    },
    {
      id: 'const_newton',
      code: '♉ 제2성좌',
      name: '뉴턴-라이프니츠 미적분 성좌',
      color: '#38bdf8',
      stars: [
        { id: 'c2_s1', star: '★1', name: '극한 수렴의 별', formula: '$\\lim_{x\\to a}\\dfrac{f(x)-f(a)}{x-a}=f\\prime(a)$', buff: '전투 시작 시 기하 필살기 게이지 +20% 선충전' },
        { id: 'c2_s2', star: '★★2', name: '도함수 접선의 별', formula: '$y - f(t) = f\\prime(t)(x - t)$', buff: '15초 이내 스피드 크리티컬 판정 시간 +5초 연장 (20초)' },
        { id: 'c2_s3', star: '★★★3', name: '정적분 넓이의 초신성', formula: '$S = \\dfrac{|a|(\\beta-\\alpha)^3}{6}$', buff: '🌟 기하 통찰 필살기 발동 시 +30 XP 즉시 획득' }
      ]
    },
    {
      id: 'const_dandelin',
      code: '♊ 제3성좌',
      name: '단델린-유클리드 기하·벡터 성좌',
      color: '#34d399',
      stars: [
        { id: 'c3_s1', star: '★1', name: '피타고라스 직각의 별', formula: '$a^2 + b^2 = c^2$', buff: '디딤돌 보호막 최대 내구도 및 시작 보호막 100% 고정' },
        { id: 'c3_s2', star: '★★2', name: '단델린 초점의 별', formula: '$c^2 = a^2 \\mp b^2$', buff: 'min7014 비급서 탐구 시 XP 보상 2배 (+30 XP)' },
        { id: 'c3_s3', star: '★★★3', name: '정사영과 공간의 제왕성', formula: '$S\\prime = S\\cos\\theta$', buff: '3단계 본문항 총공격(Q.E.D.) 성공 시 +25 XP 추가' }
      ]
    },
    {
      id: 'const_pascal',
      code: '♋ 제4성좌',
      name: '파스칼-가우스 확률·통계 성좌',
      color: '#a78bfa',
      stars: [
        { id: 'c4_s1', star: '★1', name: '여사건 전환의 별', formula: '$P(A^c) = 1 - P(A)$', buff: '오답 발생 시 필살기 충전량 +35%로 상승' },
        { id: 'c4_s2', star: '★★2', name: '조건부확률 축소의 별', formula: '$P(B|A) = \\dfrac{P(A\\cap B)}{P(A)}$', buff: 'FEVER RUSH 배율 1.5배 ➔ 1.8배로 강화' },
        { id: 'c4_s3', star: '★★★3', name: '표준정규분포 만점 수렴성', formula: '$Z = \\dfrac{X - m}{\\sigma}$', buff: '60초 스피드 블리츠 시작 시간 +10초 연장 (70초)' }
      ]
    }
  ];

  function getTodayKey() {
    var now = new Date();
    var kst = new Date(now.getTime() + (9 * 60 * 60 * 1000));
    return kst.toISOString().slice(0, 10);
  }

  function ensureDailyQuests(dq) {
    var today = getTodayKey();
    if (!dq || dq.date !== today) {
      return {
        date: today,
        stepsCleared: 0,
        archiveSummoned: 0,
        grimoireOpened: 0,
        chestClaimed: false
      };
    }
    return {
      date: today,
      stepsCleared: dq.stepsCleared || 0,
      archiveSummoned: dq.archiveSummoned || 0,
      grimoireOpened: dq.grimoireOpened || 0,
      chestClaimed: !!dq.chestClaimed
    };
  }

  // 🎨 [designer 에이전트 3대 비주얼 테마 스킨 팔레트: Cosmic / Sanctuary / Euclid]
  var QUEST_THEMES = {
    cosmic: {
      id: 'cosmic',
      cssClass: 'theme-cosmic',
      name: '🌌 코스믹 아틀리에',
      shortLabel: '🌌 코스믹',
      cycleLabel: '🎨 테마: 🌌 코스믹 (클릭 ➔ 🧘 사색 서재 / 📜 유클리드)',
      hubBg: 'linear-gradient(180deg, #060b19 0%, #0f1b33 100%)',
      hubBorder: 'rgba(56, 189, 248, 0.34)',
      dockBg: 'rgba(15, 23, 42, 0.72)',
      dockBorder: 'rgba(56, 189, 248, 0.28)',
      accent: '#38bdf8',
      accentSub: '#34d399',
      canvasBgStops: ['#0f2847', '#081428', '#060b19'],
      battleBgStops: ['#172554', '#0b132b', '#060b19'],
      battleHeaderGrad: 'linear-gradient(135deg, #060b19 0%, #1e3a8a 100%)',
      gridHighlight: 'rgba(56, 189, 248, 0.45)',
      gridBase: 'rgba(56, 189, 248, 0.13)'
    },
    sanctuary: {
      id: 'sanctuary',
      cssClass: 'theme-sanctuary',
      name: '🧘 플라톤의 사색 서재',
      shortLabel: '🧘 사색 서재',
      cycleLabel: '🎨 테마: 🧘 사색 서재 (클릭 ➔ 📜 유클리드 / 🌌 코스믹)',
      hubBg: 'linear-gradient(180deg, #110e2e 0%, #1e1848 100%)',
      hubBorder: 'rgba(167, 139, 250, 0.45)',
      dockBg: 'rgba(28, 22, 66, 0.76)',
      dockBorder: 'rgba(167, 139, 250, 0.38)',
      accent: '#a78bfa',
      accentSub: '#5eead4',
      canvasBgStops: ['#2a1d62', '#17113b', '#110e2e'],
      battleBgStops: ['#2e1065', '#18113c', '#110e2e'],
      battleHeaderGrad: 'linear-gradient(135deg, #110e2e 0%, #4c1d95 100%)',
      gridHighlight: 'rgba(167, 139, 250, 0.48)',
      gridBase: 'rgba(94, 234, 212, 0.14)'
    },
    euclid: {
      id: 'euclid',
      cssClass: 'theme-euclid',
      name: '📜 유클리드 왕립 아카데미',
      shortLabel: '📜 유클리드',
      cycleLabel: '🎨 테마: 📜 유클리드 (클릭 ➔ 🌌 코스믹 / 🧘 사색 서재)',
      hubBg: 'linear-gradient(180deg, #0b1528 0%, #172742 100%)',
      hubBorder: 'rgba(245, 158, 11, 0.48)',
      dockBg: 'rgba(18, 30, 52, 0.80)',
      dockBorder: 'rgba(245, 158, 11, 0.38)',
      accent: '#f59e0b',
      accentSub: '#38bdf8',
      canvasBgStops: ['#1e293b', '#111c33', '#0b1528'],
      battleBgStops: ['#1e293b', '#111a2e', '#0b1528'],
      battleHeaderGrad: 'linear-gradient(135deg, #0b1528 0%, #334155 100%)',
      gridHighlight: 'rgba(245, 158, 11, 0.46)',
      gridBase: 'rgba(226, 232, 240, 0.14)'
    }
  };

  function injectDesignerStylesheet() {
    if (typeof document === 'undefined') return;
    if (document.getElementById('matheduQuestDesignSystem')) return;
    var styleEl = document.createElement('style');
    styleEl.id = 'matheduQuestDesignSystem';
    styleEl.textContent = [
      '@keyframes questSanctuaryPulse {',
      '  0%, 100% {',
      '    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.55), 0 0 28px rgba(139, 92, 246, 0.38), 0 24px 52px rgba(0, 0, 0, 0.6);',
      '    border-color: #a78bfa !important;',
      '  }',
      '  50% {',
      '    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.72), 0 0 42px rgba(251, 191, 36, 0.45), 0 24px 52px rgba(0, 0, 0, 0.65);',
      '    border-color: #fbbf24 !important;',
      '  }',
      '}',
      '.quest-console-shell {',
      '  border-radius: 22px;',
      '  padding: 20px;',
      '  color: #ffffff;',
      '  backdrop-filter: blur(16px);',
      '  -webkit-backdrop-filter: blur(16px);',
      '  transition: background 0.38s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.38s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.38s ease;',
      '}',
      '.quest-console-shell.theme-cosmic {',
      '  background: linear-gradient(180deg, #060b19 0%, #0f1b33 100%);',
      '  border: 1.5px solid rgba(56, 189, 248, 0.34);',
      '  box-shadow: 0 18px 42px rgba(6, 11, 25, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.08);',
      '}',
      '.quest-console-shell.theme-sanctuary {',
      '  background: linear-gradient(180deg, #110e2e 0%, #1e1848 100%);',
      '  border: 1.5px solid rgba(167, 139, 250, 0.46);',
      '  box-shadow: 0 18px 42px rgba(17, 14, 46, 0.48), inset 0 1px 0 rgba(196, 181, 253, 0.14);',
      '}',
      '.quest-console-shell.theme-euclid {',
      '  background: linear-gradient(180deg, #0b1528 0%, #172742 100%);',
      '  border: 1.5px solid rgba(245, 158, 11, 0.5);',
      '  box-shadow: 0 18px 42px rgba(11, 21, 40, 0.46), inset 0 1px 0 rgba(251, 191, 36, 0.14);',
      '}',
      '.quest-hud-dock {',
      '  backdrop-filter: blur(16px);',
      '  -webkit-backdrop-filter: blur(16px);',
      '  border-radius: 15px;',
      '  padding: 11px 16px;',
      '  transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);',
      '}',
      '.quest-micro-btn {',
      '  transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.22s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.2s ease, background 0.2s ease;',
      '}',
      '.quest-micro-btn:hover:not(:disabled) {',
      '  transform: translateY(-1.5px);',
      '  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.24);',
      '}',
      '.quest-micro-btn:active:not(:disabled) {',
      '  transform: translateY(0) scale(0.985);',
      '}',
      '.quest-battle-modal-card {',
      '  transition: border-color 0.32s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.32s cubic-bezier(0.22, 1, 0.36, 1);',
      '}',
      '.quest-battle-modal-card.quest-meditate-active {',
      '  animation: questSanctuaryPulse 3.6s ease-in-out infinite;',
      '}',
      '.quest-battle-stem {',
      '  font-size: 15px;',
      '  font-weight: 700;',
      '  color: #0f172a;',
      '  line-height: 1.72;',
      '  letter-spacing: -0.01em;',
      '  margin-bottom: 14px;',
      '  padding: 14px 18px;',
      '  background: #ffffff;',
      '  border: 1.5px solid #cbd5e1;',
      '  border-radius: 14px;',
      '  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);',
      '  transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);',
      '}',
      '.quest-battle-stem.quest-meditate-active {',
      '  background: linear-gradient(180deg, #faf5ff 0%, #ffffff 100%);',
      '  animation: questSanctuaryPulse 3.6s ease-in-out infinite;',
      '}',
      '.quest-opt-btn {',
      '  width: 100%;',
      '  text-align: left;',
      '  padding: 12px 16px;',
      '  border-radius: 13px;',
      '  border: 1.5px solid #cbd5e1;',
      '  background: #ffffff;',
      '  color: #0f172a;',
      '  font-size: 14.5px;',
      '  font-weight: 600;',
      '  line-height: 1.72;',
      '  display: flex;',
      '  align-items: center;',
      '  gap: 12px;',
      '  cursor: pointer;',
      '  transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.22s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.18s ease, background-color 0.18s ease;',
      '}',
      '.quest-opt-btn:hover:not(:disabled) {',
      '  transform: translateY(-2px) scale(1.005);',
      '  border-color: #0284c7 !important;',
      '  background: #f0f9ff !important;',
      '  box-shadow: 0 8px 20px rgba(2, 132, 199, 0.14);',
      '}',
      '.quest-opt-btn:active:not(:disabled) {',
      '  transform: translateY(0) scale(0.996);',
      '}',
      '.quest-polya-pill {',
      '  padding: 5px 11px;',
      '  border-radius: 999px;',
      '  font-size: 11.5px;',
      '  font-weight: 800;',
      '  line-height: 1.4;',
      '  cursor: pointer;',
      '  transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1);',
      '}',
      '.quest-polya-pill:hover {',
      '  transform: translateY(-1.5px);',
      '  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15);',
      '}'
    ].join('\n');
    document.head.appendChild(styleEl);
  }

  function loadQuestState() {
    try {
      var raw = localStorage.getItem(QUEST_STATE_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        var validSkin = (parsed.themeSkin === 'sanctuary' || parsed.themeSkin === 'euclid' || parsed.themeSkin === 'cosmic')
          ? parsed.themeSkin
          : 'cosmic';
        return {
          csatScore: typeof parsed.csatScore === 'number' ? parsed.csatScore : 0,
          clearedStages: Array.isArray(parsed.clearedStages) ? parsed.clearedStages : [],
          emblems: Array.isArray(parsed.emblems) ? parsed.emblems : [],
          combo: typeof parsed.combo === 'number' ? parsed.combo : 0,
          shieldHp: typeof parsed.shieldHp === 'number' ? parsed.shieldHp : 100,
          ultimateGauge: typeof parsed.ultimateGauge === 'number' ? parsed.ultimateGauge : 100,
          activeWorldId: parsed.activeWorldId || 'w1',
          summonedCount: parsed.summonedCount || 0,
          soundEnabled: typeof parsed.soundEnabled === 'boolean' ? parsed.soundEnabled : true,
          themeSkin: validSkin,
          blitzBestScore: parsed.blitzBestScore || 0,
          equippedRelics: Array.isArray(parsed.equippedRelics) ? parsed.equippedRelics.slice(0, 3) : ['relic_gauss'],
          unlockedRelics: Array.isArray(parsed.unlockedRelics) ? parsed.unlockedRelics : ['relic_gauss', 'relic_dandelin', 'relic_pascal'],
          constellationStars: Array.isArray(parsed.constellationStars) ? parsed.constellationStars : ['c1_s1'],
          dailyQuests: ensureDailyQuests(parsed.dailyQuests)
        };
      }
    } catch (e) {}
    return {
      csatScore: 0,
      clearedStages: [],
      emblems: [],
      combo: 0,
      shieldHp: 100,
      ultimateGauge: 100,
      activeWorldId: 'w1',
      summonedCount: 0,
      soundEnabled: true,
      themeSkin: 'cosmic',
      blitzBestScore: 0,
      equippedRelics: ['relic_gauss'],
      unlockedRelics: ['relic_gauss', 'relic_dandelin', 'relic_pascal'],
      constellationStars: ['c1_s1'],
      dailyQuests: ensureDailyQuests(null)
    };
  }

  function saveQuestState(st) {
    try {
      localStorage.setItem(QUEST_STATE_KEY, JSON.stringify(st));
    } catch (e) {}
  }

  function typesetMath(el) {
    if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
      window.MathJax.typesetPromise(el ? [el] : undefined).catch(function() {});
    }
  }

  // =========================================================================
  // 🌐 3D 수학 기하 프로젝션 & 파티클 물리 엔진 (mathteacher 3D Parametric Engine)
  // =========================================================================
  var PHI = (1 + Math.sqrt(5)) / 2;
  var ICOSA_VERTS = [
    [0, 1, PHI], [0, -1, PHI], [0, 1, -PHI], [0, -1, -PHI],
    [1, PHI, 0], [-1, PHI, 0], [1, -PHI, 0], [-1, -PHI, 0],
    [PHI, 0, 1], [-PHI, 0, 1], [PHI, 0, -1], [-PHI, 0, -1]
  ];
  var ICOSA_EDGES = [];
  (function initIcosaEdges() {
    for (var i = 0; i < ICOSA_VERTS.length; i++) {
      for (var j = i + 1; j < ICOSA_VERTS.length; j++) {
        var dx = ICOSA_VERTS[i][0] - ICOSA_VERTS[j][0];
        var dy = ICOSA_VERTS[i][1] - ICOSA_VERTS[j][1];
        var dz = ICOSA_VERTS[i][2] - ICOSA_VERTS[j][2];
        var d2 = dx * dx + dy * dy + dz * dz;
        if (Math.abs(d2 - 4.0) < 0.25) {
          ICOSA_EDGES.push([i, j]);
        }
      }
    }
  })();

  function rotate3D(x, y, z, rx, ry, rz) {
    // Rotate around X
    var cosX = Math.cos(rx), sinX = Math.sin(rx);
    var y1 = y * cosX - z * sinX;
    var z1 = y * sinX + z * cosX;
    var x1 = x;
    // Rotate around Y
    var cosY = Math.cos(ry), sinY = Math.sin(ry);
    var x2 = x1 * cosY + z1 * sinY;
    var z2 = -x1 * sinY + z1 * cosY;
    var y2 = y1;
    // Rotate around Z
    if (rz) {
      var cosZ = Math.cos(rz), sinZ = Math.sin(rz);
      var x3 = x2 * cosZ - y2 * sinZ;
      var y3 = x2 * sinZ + y2 * cosZ;
      return { x: x3, y: y3, z: z2 };
    }
    return { x: x2, y: y2, z: z2 };
  }

  function project3D(pt, cx, cy, fov, camDist, zoom) {
    var z = pt.z + camDist;
    if (z < 0.4) z = 0.4;
    var scale = (fov * zoom) / z;
    return {
      x: cx + pt.x * scale,
      y: cy - pt.y * scale,
      z: z,
      scale: scale
    };
  }

  // 별자리 배경 파티클
  var STAR_FIELD = [];
  for (var si = 0; si < 75; si++) {
    STAR_FIELD.push({
      x: (Math.random() - 0.5) * 9,
      y: (Math.random() - 0.5) * 6,
      z: (Math.random() - 0.5) * 7,
      size: 0.8 + Math.random() * 1.6,
      alpha: 0.25 + Math.random() * 0.65
    });
  }

  var QuestEngine = {
    state: loadQuestState(),
    activeStage: null,
    activeStepIdx: 0,
    shardCache: {},

    // 3D Viewport 상태
    view3D: {
      rx: 0.42,
      ry: -0.55,
      zoom: 1.05,
      autoRotate: true,
      showXray: true,
      galaxyMode: false,
      dragging: false,
      lastX: 0,
      lastY: 0,
      time: 0,
      animId: null,
      nodeScreenCoords: []
    },

    // 3D Battle Arena 상태
    battle3D: {
      rx: 0.35,
      ry: 0.0,
      zoom: 1.0,
      time: 0,
      shake: 0,
      laserTimer: 0,
      supernovaTimer: 0,
      allOutSlashTimer: 0,
      shieldFlash: 0,
      stepStartTime: 0,
      stepAttempts: 0,
      stageMistakes: 0,
      eulerShieldUsed: false,
      particles: [],
      floatingTexts: [],
      animId: null
    },

    // 🧠 깊은 사색과 유레카 (Deep Contemplation & Eureka) 상태
    insightGauge: 0,
    meditateMode: false,
    polyaSteps: { s1: false, s2: false, s3: false },
    scratchpadOpen: false,
    scratchpadUsed: false,
    scratchpadColor: '#38bdf8',
    scratchpadDrawing: false,
    eurekaReadyNotified: false,

    // =========================================================================
    // 🃏 수학자의 성물(Relics) & 🌌 4대 수학 성좌(Constellations) 헬퍼 및 모달 시스템
    // =========================================================================
    hasRelic: function(relicId) {
      var eq = (this.state && Array.isArray(this.state.equippedRelics)) ? this.state.equippedRelics : [];
      return eq.indexOf(relicId) !== -1;
    },

    getRelicById: function(relicId) {
      for (var i = 0; i < MATH_RELICS.length; i++) {
        if (MATH_RELICS[i].id === relicId) return MATH_RELICS[i];
      }
      return null;
    },

    hasConstellationStar: function(starId) {
      var cs = (this.state && Array.isArray(this.state.constellationStars)) ? this.state.constellationStars : [];
      return cs.indexOf(starId) !== -1;
    },

    getFeverThreshold: function() {
      return (this.hasRelic('relic_pascal') || this.hasRelic('relic_gauss')) ? 2 : 3;
    },

    getFeverMultiplier: function() {
      var mult = this.hasConstellationStar('c4_s2') ? 1.8 : 1.5;
      if (this.hasRelic('relic_pascal')) mult += 0.2;
      return mult;
    },

    getActiveSynergies: function() {
      var list = [];
      if (this.hasRelic('relic_fermat') && this.hasRelic('relic_leibniz')) {
        list.push({
          id: 'syn_ftc',
          name: '⚡ [미적분학의 기본정리 시너지]',
          desc: '페르마의 극치 + 라이프니츠 태엽 공명: 모든 단계 XP +20% 증폭'
        });
      }
      if (this.hasRelic('relic_dandelin') && (this.hasRelic('relic_descartes') || this.hasRelic('relic_cauchy'))) {
        list.push({
          id: 'syn_geo',
          name: '🔮 [동적 기하 각성 시너지]',
          desc: '단델린의 쌍구 + 데카르트/코시 공명: 필살기 게이지 충전 +30% 가속'
        });
      }
      if (this.hasRelic('relic_gauss') && (this.hasRelic('relic_pascal') || this.hasRelic('relic_bernoulli'))) {
        list.push({
          id: 'syn_prob',
          name: '🎲 [이산수학 대칭 시너지]',
          desc: '가우스의 저울 + 파스칼/베르누이 공명: 보스 격파 시 수능 점수 +1점 추가'
        });
      }
      if (this.hasRelic('relic_archimedes') && (this.hasRelic('relic_dandelin') || this.hasRelic('relic_descartes'))) {
        list.push({
          id: 'syn_eureka',
          name: '🧘 [플라톤 아카데미아의 깊은 사색 시너지]',
          desc: '아르키메데스 모래시계 + 단델린/데카르트 공명: 단계 진입 시 사색 통찰 게이지 35% 선충전'
        });
      }
      return list;
    },

    spawnFloatingText: function(text, color, offsetY) {
      this.battle3D.floatingTexts.push({
        text: text,
        color: color || '#fde047',
        x: (Math.random() - 0.5) * 36,
        y: (typeof offsetY === 'number' ? offsetY : -8),
        vy: -0.65,
        life: 1.0
      });
    },

    // =========================================================================
    // 🧠 깊은 사색과 수학적 유레카 (Deep Contemplation & Eureka) 메서드
    // =========================================================================
    resetStepContemplation: function() {
      var hasEurekaSyn = this.hasRelic('relic_archimedes') && (this.hasRelic('relic_dandelin') || this.hasRelic('relic_descartes'));
      this.insightGauge = hasEurekaSyn ? 35 : (this.hasRelic('relic_archimedes') ? 20 : 0);
      this.polyaSteps = { s1: false, s2: false, s3: false };
      this.scratchpadUsed = false;
      this.eurekaReadyNotified = false;
    },

    updateInsightGaugeDOM: function() {
      var pct = Math.min(100, Math.max(0, Math.round(this.insightGauge || 0)));
      var fillEl = document.getElementById('questInsightGaugeFill');
      var txtEl = document.getElementById('questInsightGaugeText');
      var badgeEl = document.getElementById('questInsightStatusBadge');

      if (fillEl) {
        fillEl.style.width = pct + '%';
        fillEl.style.background = pct >= 90
          ? 'linear-gradient(90deg,#f59e0b,#fde047,#10b981)'
          : (pct >= 50 ? 'linear-gradient(90deg,#0284c7,#38bdf8,#a78bfa)' : 'linear-gradient(90deg,#64748b,#38bdf8)');
      }
      if (txtEl) {
        txtEl.textContent = pct + '%';
      }
      if (badgeEl) {
        if (pct >= 90) {
          badgeEl.innerHTML = '🧠 DEEP EUREKA 준비 완료! (정답 시 +40 XP · 필살기 +35% · 수능 +1점)';
          badgeEl.style.background = 'linear-gradient(135deg,#f59e0b 0%,#d97706 100%)';
          badgeEl.style.color = '#ffffff';
        } else if (pct >= 50) {
          badgeEl.innerHTML = '💡 깊은 논리 숙고 중 (THOUGHTFUL SOLVE · 정답 시 +20 XP)';
          badgeEl.style.background = '#e0f2fe';
          badgeEl.style.color = '#0369a1';
        } else {
          badgeEl.innerHTML = '⏳ 문제를 읽고 조건을 분석하며 통찰력을 모으는 중...';
          badgeEl.style.background = '#f1f5f9';
          badgeEl.style.color = '#475569';
        }
      }
      if (pct >= 90 && !this.eurekaReadyNotified) {
        this.eurekaReadyNotified = true;
        this.playGameSfx('eureka');
        this.spawnFloatingText('🧠 DEEP EUREKA READY! (사색 통찰 90% 돌파)', '#fde047', -14);
      }
    },

    toggleMeditateMode: function() {
      this.meditateMode = !this.meditateMode;
      if (this.meditateMode) {
        this.view3D.showXray = true;
        this.playGameSfx('meditate');
        this.spawnFloatingText('🧘 플라톤의 사색 결계 발동! (시간 정지 & 통찰 가속)', '#38bdf8', -12);
      } else {
        this.playGameSfx('hit');
      }

      var modalCard = document.getElementById('questBattleModalCard');
      if (modalCard) {
        modalCard.classList.toggle('quest-meditate-active', this.meditateMode);
      }
      var stemBox = document.getElementById('questBattleStemBox');
      if (stemBox) {
        stemBox.classList.toggle('quest-meditate-active', this.meditateMode);
      }

      var btnBattle = document.getElementById('btnToggleMeditateBattle');
      if (btnBattle) {
        btnBattle.innerHTML = this.meditateMode
          ? '🧘 사색 모드 ON (결계 감속 · 통찰 2배 충전 중)'
          : '🧘 사색 모드 (생각 시간 갖기)';
        btnBattle.style.background = this.meditateMode
          ? 'linear-gradient(135deg,#7c3aed 0%,#0d9488 100%)'
          : 'rgba(255,255,255,0.16)';
        btnBattle.style.borderColor = this.meditateMode ? '#fbbf24' : 'rgba(255,255,255,0.28)';
      }

      var btnBlitz = document.getElementById('btnToggleMeditateBlitz');
      if (btnBlitz) {
        btnBlitz.innerHTML = this.meditateMode
          ? '🧘 사색 일시정지 ON (타이머 정지됨 · 클릭 시 재개)'
          : '🧘 사색 모드 (타이머 일시정지 & 생각 시간 갖기)';
        btnBlitz.style.background = this.meditateMode
          ? 'linear-gradient(135deg,#7c3aed 0%,#0d9488 100%)'
          : 'rgba(255,255,255,0.16)';
      }
    },

    togglePolyaStep: function(stepNum) {
      var stg = this.activeStage;
      var curStep = (stg && stg.steps) ? (stg.steps[this.activeStepIdx] || stg.steps[0]) : null;
      var key = 's' + stepNum;
      if (!this.polyaSteps) this.polyaSteps = { s1: false, s2: false, s3: false };

      if (!this.polyaSteps[key]) {
        this.polyaSteps[key] = true;
        var gain = (stepNum === 1) ? 30 : 35;
        this.insightGauge = Math.min(100, (this.insightGauge || 0) + gain);
        this.playGameSfx('meditate');
      }

      if (this.polyaSteps.s1 && this.polyaSteps.s2 && this.polyaSteps.s3) {
        this.insightGauge = 100;
      }
      this.updateInsightGaugeDOM();

      var btn = document.getElementById('btnPolyaStep' + stepNum);
      if (btn) {
        btn.style.background = '#dcfce7';
        btn.style.borderColor = '#22c55e';
        btn.style.color = '#15803d';
      }

      var coachBox = document.getElementById('questPolyaCoachingBox');
      if (coachBox && curStep) {
        coachBox.style.display = 'block';
        if (stepNum === 1) {
          coachBox.innerHTML = '🎯 <b>[폴리아 1단계 · 구하는 것 확인 완료 (+통찰 30%)]</b><br>' +
            '현재 <b>「' + curStep.label + '」</b>에서 최종적으로 찾아야 하는 식이나 값을 발문 끝부분에서 먼저 명확히 확인했습니다!';
          this.spawnFloatingText('🎯 폴리아 ① 구하는 것 확인! (+통찰 30%)', '#38bdf8', -10);
        } else if (stepNum === 2) {
          var symDetails = document.getElementById('questSymbolTranslatorDetails');
          if (symDetails) symDetails.open = true;
          coachBox.innerHTML = '🔑 <b>[폴리아 2단계 · 주어진 조건 분해 완료 (+통찰 35%)]</b><br>' +
            '제0단계 기호 번역기 마법서를 펼쳐 조건을 분해했습니다! 핵심 단서: ' + curStep.know;
          this.spawnFloatingText('🔑 폴리아 ② 조건 분해! (+통찰 35%)', '#fbbf24', -10);
        } else if (stepNum === 3) {
          this.view3D.showXray = true;
          coachBox.innerHTML = '🌉 <b>[폴리아 3단계 · 연결 공식·보조선 구상 완료 (+통찰 35%)]</b><br>' +
            '주어진 조건과 구하는 목표를 잇는 수학 공식·3D 기하 보조선을 연결했습니다. 이제 확신을 갖고 선지를 선택하세요!';
          this.spawnFloatingText('🌉 폴리아 ③ 연결 공식 구상! (+통찰 35%)', '#34d399', -10);
        }
        typesetMath(coachBox);
      }
    },

    toggleScratchpad: function() {
      this.scratchpadOpen = !this.scratchpadOpen;
      var wrap = document.getElementById('questScratchpadWrap');
      var btn = document.getElementById('btnToggleScratchpad');
      if (wrap) {
        wrap.style.display = this.scratchpadOpen ? 'block' : 'none';
      }
      if (btn) {
        btn.innerHTML = this.scratchpadOpen ? '✏️ 생각 연습장 닫기' : '✏️ 생각 연습장 (Scratchpad)';
        btn.style.background = this.scratchpadOpen ? '#0284c7' : '#f0f9ff';
        btn.style.color = this.scratchpadOpen ? '#ffffff' : '#0369a1';
      }
      if (this.scratchpadOpen) {
        this.initScratchpadCanvas();
      }
    },

    setScratchpadColor: function(col) {
      this.scratchpadColor = col || '#38bdf8';
    },

    clearScratchpad: function() {
      var c = document.getElementById('questScratchpadCanvas');
      if (!c) return;
      this.drawScratchpadGrid(c);
    },

    drawScratchpadGrid: function(c) {
      var ctx = c.getContext('2d');
      var w = c.width, h = c.height;
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, w, h);

      // 모눈종이 격자 (20px 간격)
      ctx.strokeStyle = 'rgba(148,163,184,0.14)';
      ctx.lineWidth = 1;
      for (var x = 0; x <= w; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }
      for (var y = 0; y <= h; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      // 데카르트 십자 기준 보조선
      ctx.strokeStyle = 'rgba(56,189,248,0.24)';
      ctx.beginPath();
      ctx.moveTo(w * 0.5, 0);
      ctx.lineTo(w * 0.5, h);
      ctx.moveTo(0, h * 0.5);
      ctx.lineTo(w, h * 0.5);
      ctx.stroke();
    },

    initScratchpadCanvas: function() {
      var self = this;
      var c = document.getElementById('questScratchpadCanvas');
      if (!c) return;
      if (!c.getAttribute('data-initialized')) {
        c.setAttribute('data-initialized', '1');
        this.drawScratchpadGrid(c);
      }
      var ctx = c.getContext('2d');
      var lastPt = null;

      function getPos(ev) {
        var rect = c.getBoundingClientRect();
        var clientX = (ev.touches && ev.touches.length) ? ev.touches[0].clientX : ev.clientX;
        var clientY = (ev.touches && ev.touches.length) ? ev.touches[0].clientY : ev.clientY;
        return {
          x: (clientX - rect.left) * (c.width / rect.width),
          y: (clientY - rect.top) * (c.height / rect.height)
        };
      }

      function markScratchpadActive() {
        if (!self.scratchpadUsed) {
          self.scratchpadUsed = true;
          self.insightGauge = Math.min(100, (self.insightGauge || 0) + 40);
          self.updateInsightGaugeDOM();
          self.spawnFloatingText('✍️ 데카르트 연습장 활성화! (+통찰 40%)', '#38bdf8', -10);
          var bdg = document.getElementById('questScratchpadStatusBadge');
          if (bdg) {
            bdg.innerHTML = '✍️ 데카르트 연습장 활성화됨! (통찰 +40% 충전 완료 · 정답 시 +15 XP 보너스)';
            bdg.style.color = '#34d399';
          }
        }
      }

      c.onmousedown = function(ev) {
        self.scratchpadDrawing = true;
        lastPt = getPos(ev);
        markScratchpadActive();
      };
      c.onmousemove = function(ev) {
        if (!self.scratchpadDrawing || !lastPt) return;
        var pt = getPos(ev);
        ctx.strokeStyle = self.scratchpadColor || '#38bdf8';
        ctx.lineWidth = 2.6;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(lastPt.x, lastPt.y);
        ctx.lineTo(pt.x, pt.y);
        ctx.stroke();
        lastPt = pt;
      };
      c.onmouseup = function() {
        self.scratchpadDrawing = false;
        lastPt = null;
      };
      c.onmouseleave = function() {
        self.scratchpadDrawing = false;
        lastPt = null;
      };

      c.ontouchstart = function(ev) {
        ev.preventDefault();
        self.scratchpadDrawing = true;
        lastPt = getPos(ev);
        markScratchpadActive();
      };
      c.ontouchmove = function(ev) {
        if (!self.scratchpadDrawing || !lastPt) return;
        ev.preventDefault();
        var pt = getPos(ev);
        ctx.strokeStyle = self.scratchpadColor || '#38bdf8';
        ctx.lineWidth = 2.6;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(lastPt.x, lastPt.y);
        ctx.lineTo(pt.x, pt.y);
        ctx.stroke();
        lastPt = pt;
      };
      c.ontouchend = function() {
        self.scratchpadDrawing = false;
        lastPt = null;
      };
    },

    openRelicDraftModal: function() {
      this.playGameSfx('summon');
      var existing = document.getElementById('matheduRelicDraftModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduRelicDraftModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:100000;background:rgba(4,8,22,0.92);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:14px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      // 무작위 3택1 드래프트 후보 추출
      var shuffled = MATH_RELICS.slice().sort(function() { return Math.random() - 0.5; });
      var draft3 = shuffled.slice(0, 3);
      var eq = this.state.equippedRelics || [];
      var synergies = this.getActiveSynergies();

      var draftCardsHtml = draft3.map(function(r) {
        var isEq = eq.indexOf(r.id) !== -1;
        var rarityCol = r.rarity === 'SSR' ? '#f59e0b' : (r.rarity === 'SR' ? '#38bdf8' : '#34d399');
        return '<div style="background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%);border:2px solid ' + (isEq ? '#fde047' : rarityCol) + ';border-radius:16px;padding:14px;display:flex;flex-direction:column;justify-content:space-between;gap:10px;box-shadow:0 8px 24px rgba(0,0,0,0.45)">' +
          '<div>' +
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">' +
              '<span style="font-size:24px">' + r.icon + '</span>' +
              '<span style="padding:2px 8px;border-radius:999px;background:' + rarityCol + ';color:#0f172a;font-size:10.5px;font-weight:900">' + r.rarity + ' 성물</span>' +
            '</div>' +
            '<div style="font-size:15px;font-weight:900;color:#ffffff;margin-bottom:4px">' + r.name + '</div>' +
            '<div style="padding:5px 8px;border-radius:8px;background:rgba(255,255,255,0.07);color:#fde047;font-size:12px;font-weight:700;margin-bottom:6px">' + r.formula + '</div>' +
            '<div style="font-size:11.5px;color:#cbd5e1;line-height:1.5;margin-bottom:8px">💡 ' + r.intuition + '</div>' +
            '<div style="font-size:12px;font-weight:800;color:#34d399;line-height:1.45">⚡ 전투 효과: ' + r.effectDesc + '</div>' +
          '</div>' +
          '<button type="button" onclick="window.MatheduQuest.toggleEquipRelic(\'' + r.id + '\')" ' +
            'style="width:100%;padding:9px;border-radius:10px;border:none;background:' + (isEq ? 'linear-gradient(135deg,#059669 0%,#10b981 100%)' : 'linear-gradient(135deg,#f59e0b 0%,#ea580c 100%)') + ';color:#ffffff;font-size:12px;font-weight:900;cursor:pointer">' +
            (isEq ? '✅ 장착 중 (클릭 시 해제)' : '🃏 이 성물 선택·장착하기') +
          '</button>' +
        '</div>';
      }).join('');

      var allRelicsHtml = MATH_RELICS.map(function(r) {
        var isEq = eq.indexOf(r.id) !== -1;
        return '<button type="button" onclick="window.MatheduQuest.toggleEquipRelic(\'' + r.id + '\')" ' +
          'style="padding:7px 11px;border-radius:10px;border:1.5px solid ' + (isEq ? '#fbbf24' : '#cbd5e1') + ';background:' + (isEq ? '#fef3c7' : '#f8fafc') + ';color:#0f172a;font-size:12px;font-weight:800;cursor:pointer;display:inline-flex;align-items:center;gap:5px">' +
          '<span>' + r.icon + ' ' + r.name + '</span>' +
          '<span style="font-size:10px;padding:1px 5px;border-radius:999px;background:' + (isEq ? '#d97706' : '#64748b') + ';color:#fff">' + (isEq ? '장착중' : r.rarity) + '</span>' +
        '</button>';
      }).join('');

      var synHtml = synergies.length
        ? synergies.map(function(s) {
            return '<div style="padding:6px 10px;border-radius:8px;background:#fef3c7;border:1px solid #f59e0b;color:#92400e;font-size:12px;font-weight:800">' + s.name + ' — ' + s.desc + '</div>';
          }).join('')
        : '<div style="font-size:12px;color:#64748b">성물을 2~3개 조합하면 특별 수학 시너지(미적분학의 기본정리, 동적 기하 각성, 이산수학 대칭)가 발동합니다!</div>';

      existing.innerHTML =
        '<div style="width:100%;max-width:760px;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 24px 52px rgba(0,0,0,0.65);border:2px solid #f59e0b;max-height:94vh;display:flex;flex-direction:column">' +
          '<div style="background:linear-gradient(135deg,#070d1e 0%,#4c1d95 100%);color:#ffffff;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;gap:10px">' +
            '<div>' +
              '<div style="font-size:11px;color:#fbbf24;font-weight:800">🃏 로그라이크 수학자의 성물 3택1 드래프트 & 덱 빌딩 (최대 3개 장착)</div>' +
              '<div style="font-size:17px;font-weight:900;margin-top:2px">🏛️ 위대한 수학자 10인의 성물 보관소 (' + eq.length + ' / 3 슬롯 장착 중)</div>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<button type="button" onclick="window.MatheduQuest.openRelicDraftModal()" style="padding:6px 12px;border-radius:999px;border:1px solid #fbbf24;background:rgba(251,191,36,0.2);color:#fde047;font-size:11.5px;font-weight:800;cursor:pointer">🎲 3택1 다시 뽑기</button>' +
              '<button type="button" onclick="window.MatheduQuest.closeRelicDraftModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.16);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
            '</div>' +
          '</div>' +
          '<div style="padding:16px 20px;overflow-y:auto;flex:1">' +
            '<div style="margin-bottom:12px;font-size:13px;font-weight:800;color:#0f172a">✨ 오늘의 3택 1 성물 드래프트 추천 카드 (원하는 성물을 클릭해 즉시 장착하세요!)</div>' +
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-bottom:16px">' +
              draftCardsHtml +
            '</div>' +
            '<div style="margin-bottom:14px;padding:12px;border-radius:12px;background:#fffbeb;border:1px solid #fde68a">' +
              '<div style="font-size:12.5px;font-weight:900;color:#92400e;margin-bottom:6px">🔥 현재 발동 중인 수학 성물 덱 시너지</div>' +
              '<div style="display:flex;flex-direction:column;gap:6px">' + synHtml + '</div>' +
            '</div>' +
            '<div style="padding:12px;border-radius:12px;background:#f1f5f9;border:1px solid #cbd5e1">' +
              '<div style="font-size:12.5px;font-weight:900;color:#0f172a;margin-bottom:8px">📚 전체 10종 수학 성물 도감 (클릭하여 장착 슬롯 최대 3개 자유 교체)</div>' +
              '<div style="display:flex;flex-wrap:wrap;gap:6px">' + allRelicsHtml + '</div>' +
            '</div>' +
          '</div>' +
        '</div>';

      typesetMath(existing);
    },

    toggleEquipRelic: function(relicId) {
      var eq = Array.isArray(this.state.equippedRelics) ? this.state.equippedRelics.slice() : [];
      var idx = eq.indexOf(relicId);
      if (idx !== -1) {
        eq.splice(idx, 1);
        this.playGameSfx('shield');
      } else {
        if (eq.length >= 3) {
          eq.shift(); // 가장 먼저 장착한 슬롯을 교체
        }
        eq.push(relicId);
        this.playGameSfx('hit');
      }
      this.state.equippedRelics = eq;
      if (this.state.unlockedRelics.indexOf(relicId) === -1) {
        this.state.unlockedRelics.push(relicId);
      }
      saveQuestState(this.state);
      this.openRelicDraftModal();
      this.renderConsoleHub();
    },

    closeRelicDraftModal: function() {
      var m = document.getElementById('matheduRelicDraftModal');
      if (m) m.remove();
      this.renderConsoleHub();
    },

    openConstellationModal: function() {
      this.playGameSfx('summon');
      var existing = document.getElementById('matheduConstellationModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduConstellationModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:100000;background:rgba(4,8,22,0.92);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:14px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      var awakened = this.state.constellationStars || [];

      var constCardsHtml = MATH_CONSTELLATIONS.map(function(c) {
        var starsHtml = c.stars.map(function(st) {
          var isOn = awakened.indexOf(st.id) !== -1;
          return '<div onclick="window.MatheduQuest.toggleConstellationStar(\'' + st.id + '\')" ' +
            'style="padding:10px 12px;border-radius:12px;border:1.5px solid ' + (isOn ? c.color : 'rgba(255,255,255,0.15)') + ';background:' + (isOn ? 'rgba(56,189,248,0.16)' : 'rgba(255,255,255,0.04)') + ';cursor:pointer;transition:all .15s">' +
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">' +
              '<span style="font-size:12.5px;font-weight:900;color:' + (isOn ? '#fde047' : '#e2e8f0') + '">' + st.star + ' · ' + st.name + '</span>' +
              '<span style="font-size:11px;padding:2px 8px;border-radius:999px;background:' + (isOn ? '#10b981' : 'rgba(255,255,255,0.12)') + ';color:#ffffff;font-weight:800">' + (isOn ? '✨ 각성 완료' : '클릭하여 각성') + '</span>' +
            '</div>' +
            '<div style="font-size:12px;color:#93c5fd;margin-bottom:4px">공식: ' + st.formula + '</div>' +
            '<div style="font-size:11.5px;color:#34d399;font-weight:700">🌟 영구 패시브: ' + st.buff + '</div>' +
          '</div>';
        }).join('');

        return '<div style="background:linear-gradient(180deg,#09152b 0%,#0f172a 100%);border:1.5px solid ' + c.color + ';border-radius:16px;padding:14px">' +
          '<div style="font-size:14.5px;font-weight:900;color:' + c.color + ';margin-bottom:10px">' + c.code + ' · ' + c.name + '</div>' +
          '<div style="display:flex;flex-direction:column;gap:8px">' + starsHtml + '</div>' +
        '</div>';
      }).join('');

      existing.innerHTML =
        '<div style="width:100%;max-width:780px;background:#040914;color:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 24px 52px rgba(0,0,0,0.75);border:2px solid #38bdf8;max-height:94vh;display:flex;flex-direction:column">' +
          '<div style="background:linear-gradient(135deg,#070d1e 0%,#0c4a6e 100%);padding:14px 18px;display:flex;align-items:center;justify-content:space-between;gap:10px">' +
            '<div>' +
              '<div style="font-size:11px;color:#38bdf8;font-weight:800">🌌 4대 수학 성좌 각성 스킬트리 (Constellations of CSAT 100 Mastery)</div>' +
              '<div style="font-size:17px;font-weight:900;margin-top:2px">✨ 각성한 별자리: ' + awakened.length + ' / 12성 (별자리를 클릭해 영구 패시브를 각성하세요!)</div>' +
            '</div>' +
            '<button type="button" onclick="window.MatheduQuest.closeConstellationModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.16);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
          '</div>' +
          '<div style="padding:16px 20px;overflow-y:auto;flex:1;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px">' +
            constCardsHtml +
          '</div>' +
        '</div>';

      typesetMath(existing);
    },

    toggleConstellationStar: function(starId) {
      var cs = Array.isArray(this.state.constellationStars) ? this.state.constellationStars.slice() : [];
      var idx = cs.indexOf(starId);
      if (idx !== -1) {
        cs.splice(idx, 1);
        this.playGameSfx('shield');
      } else {
        cs.push(starId);
        this.playGameSfx('victory');
      }
      this.state.constellationStars = cs;
      saveQuestState(this.state);
      this.openConstellationModal();
      this.renderConsoleHub();
    },

    closeConstellationModal: function() {
      var m = document.getElementById('matheduConstellationModal');
      if (m) m.remove();
      this.renderConsoleHub();
    },

    getWorlds: function() {
      return WORLDS;
    },

    getWorldById: function(wid) {
      for (var i = 0; i < WORLDS.length; i++) {
        if (WORLDS[i].id === wid) return WORLDS[i];
      }
      return WORLDS[0];
    },

    getWorldMonumentFormulaDesc: function(wid) {
      var map = {
        w1: '📐 [3D 회전 포물면 & 원과 직선의 정사영] z = a(x²+y²) 단면 원과 접선 d = r 스파크',
        w2: '🌀 [3D 단위원 삼각함수 나선 & 지수·로그 대칭] (R cos t, R sin t, ct) 정사영 사인·코사인파',
        w3: '⚡ [3D 구분구적법 리만 적층 & 삼차함수 극값 곡면] z = ⅓x³ - x 와 정적분 원판 수렴',
        w4: '🔮 [3D 단델린의 구(Dandelin Spheres) & 원뿔곡선] 이중 원뿔 내접 두 구와 타원 초점 F₁, F₂',
        w5: '🐉 [3D (2,3)-토러스 매듭 & Frenet-Serret 벡터장] 고난도 킬러 추론 매듭 궤도와 접선·법선 벡터',
        w6: '👑 [3D 황금비 정이십면체 왕관 & 30문항 피보나치 성좌] φ = (1+√5)/2 쌍대 다면체와 수능 100점 성좌'
      };
      return map[wid] || map.w1;
    },

    getGradeRankLabel: function(score) {
      if (score >= 100) return '👑 수능 수학 100점 만점 (전국 수석 마스터)';
      if (score >= 92) return '💎 1등급 최상위권 (' + score + '점 / 100점)';
      if (score >= 84) return '🔥 1등급 진입권 (' + score + '점 / 100점)';
      if (score >= 74) return '⚡ 공통과목 마스터권 (' + score + '점 / 100점)';
      if (score >= 45) return '🌿 중위권 도약 중 (' + score + '점 / 100점)';
      return '🌱 기초 디딤돌 등반 중 (' + score + '점 / 100점)';
    },

    getThemeConfig: function(skinId) {
      var key = skinId || (this.state && this.state.themeSkin) || 'cosmic';
      return QUEST_THEMES[key] || QUEST_THEMES.cosmic;
    },

    cycleQuestTheme: function() {
      var order = ['cosmic', 'sanctuary', 'euclid'];
      var cur = (this.state && this.state.themeSkin) || 'cosmic';
      var nextIdx = (order.indexOf(cur) + 1) % order.length;
      this.setQuestTheme(order[nextIdx]);
    },

    setQuestTheme: function(skinId) {
      if (!QUEST_THEMES[skinId]) skinId = 'cosmic';
      this.state.themeSkin = skinId;
      saveQuestState(this.state);
      this.playGameSfx('meditate');
      this.renderConsoleHub();
      var battleModal = document.getElementById('matheduQuestBattleModal');
      if (battleModal && this.activeStage) {
        this.renderBattleModal();
      }
    },

    selectWorld: function(wid) {
      this.state.activeWorldId = wid;
      this.view3D.galaxyMode = false;
      saveQuestState(this.state);
      this.renderConsoleHub();
    },

    toggleXrayMode: function() {
      this.view3D.showXray = !this.view3D.showXray;
      var btn = document.getElementById('btnToggle3DXray');
      if (btn) {
        btn.innerHTML = this.view3D.showXray ? '📐 수학 보조선·정사영 투시 ON' : '📐 수학 보조선·정사영 투시 OFF';
        btn.style.background = this.view3D.showXray ? 'rgba(16,185,129,0.28)' : 'rgba(255,255,255,0.1)';
        btn.style.borderColor = this.view3D.showXray ? '#34d399' : 'rgba(255,255,255,0.2)';
      }
    },

    toggleGalaxyMode: function() {
      this.view3D.galaxyMode = !this.view3D.galaxyMode;
      var btn = document.getElementById('btnToggle3DGalaxy');
      if (btn) {
        btn.innerHTML = this.view3D.galaxyMode ? '🔭 현재 대륙 3D 모뉴먼트 집중 보기' : '🌌 6대 대륙 3D 행성계 전체 성좌 보기';
      }
    },

    resetCamera3D: function() {
      this.view3D.rx = 0.42;
      this.view3D.ry = -0.55;
      this.view3D.zoom = 1.05;
      this.view3D.autoRotate = true;
    },

    // =========================================================================
    // 🔊 무의존성 WebAudio API 신디사이저 사운드 엔진 (gamemaker SFX Engine)
    // =========================================================================
    audioCtx: null,

    playGameSfx: function(type) {
      if (this.state && this.state.soundEnabled === false) return;
      try {
        var AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        if (!this.audioCtx) {
          this.audioCtx = new AudioCtx();
        }
        var ctx = this.audioCtx;
        if (ctx.state === 'suspended') {
          ctx.resume();
        }
        var now = ctx.currentTime;

        function playTone(freq, oscType, startTime, duration, vol, endFreq) {
          var osc = ctx.createOscillator();
          var gain = ctx.createGain();
          osc.type = oscType || 'sine';
          osc.frequency.setValueAtTime(freq, startTime);
          if (endFreq) {
            osc.frequency.exponentialRampToValueAtTime(endFreq, startTime + duration);
          }
          gain.gain.setValueAtTime(vol || 0.12, startTime);
          gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(startTime);
          osc.stop(startTime + duration);
        }

        if (type === 'hit') {
          // 정답 타격 & 3D 결계 파쇄: 경쾌한 상승 아르페지오 + 레이저 톤
          playTone(523.25, 'triangle', now, 0.11, 0.14);        // C5
          playTone(659.25, 'triangle', now + 0.06, 0.12, 0.14); // E5
          playTone(783.99, 'triangle', now + 0.12, 0.16, 0.15); // G5
          playTone(1046.50, 'sine', now + 0.18, 0.24, 0.16);    // C6
          playTone(920, 'sawtooth', now, 0.18, 0.07, 240);      // Laser sweep
        } else if (type === 'shield') {
          // 오답 시 3D 허니컴 방어막 공명음
          playTone(220, 'sine', now, 0.25, 0.15, 165);
          playTone(330, 'triangle', now + 0.05, 0.25, 0.10, 247.5);
        } else if (type === 'victory') {
          // 보스 최종 격파: 웅장한 4화음 팡파르
          var notes = [523.25, 659.25, 783.99, 1046.50];
          for (var i = 0; i < notes.length; i++) {
            playTone(notes[i], 'triangle', now + i * 0.09, 0.32, 0.15);
          }
          playTone(523.25, 'sine', now + 0.36, 0.55, 0.12);
          playTone(783.99, 'triangle', now + 0.36, 0.55, 0.12);
          playTone(1046.50, 'triangle', now + 0.36, 0.60, 0.16);
        } else if (type === 'summon') {
          // 16,548문항 3D 보스 소환: 하이퍼 워프 효과음
          playTone(180, 'sine', now, 0.35, 0.14, 880);
          playTone(270, 'triangle', now + 0.06, 0.32, 0.10, 1320);
        } else if (type === 'meditate') {
          // 🧘 플라톤의 사색 결계 & 폴리아 생각 징검다리: 고요하고 따뜻한 432Hz 명상 화음
          playTone(432.0, 'sine', now, 0.55, 0.11);
          playTone(540.0, 'sine', now + 0.08, 0.55, 0.09);
          playTone(648.0, 'triangle', now + 0.16, 0.60, 0.08);
        } else if (type === 'eureka') {
          // 🧠 아르키메데스의 DEEP EUREKA!! 달성: 찬란한 황금 유레카 차임벨
          playTone(587.33, 'sine', now, 0.16, 0.14);        // D5
          playTone(739.99, 'sine', now + 0.07, 0.18, 0.14); // F#5
          playTone(880.00, 'triangle', now + 0.14, 0.22, 0.15); // A5
          playTone(1174.66, 'sine', now + 0.22, 0.48, 0.17);    // D6
        }
      } catch (e) {}
    },

    toggleSound: function() {
      this.state.soundEnabled = (this.state.soundEnabled === false) ? true : false;
      saveQuestState(this.state);
      var btn = document.getElementById('btnToggle3DSound');
      if (btn) {
        btn.innerHTML = this.state.soundEnabled ? '🔊 효과음 ON' : '🔇 효과음 OFF';
        btn.style.background = this.state.soundEnabled ? 'rgba(251,191,36,0.25)' : 'rgba(255,255,255,0.1)';
        btn.style.borderColor = this.state.soundEnabled ? '#fbbf24' : 'rgba(255,255,255,0.2)';
      }
      if (this.state.soundEnabled) {
        this.playGameSfx('hit');
      }
    },

    // =========================================================================
    // 🎨 메인 3D 수학 홀로그램 캔버스 렌더러 (60fps)
    // =========================================================================
    initMain3DCanvas: function() {
      var self = this;
      var canvas = document.getElementById('matheduQuest3DCanvas');
      if (!canvas) return;

      // 마우스 / 터치 드래그 360도 회전 및 휠 줌 바인딩
      canvas.onmousedown = function(e) {
        self.view3D.dragging = true;
        self.view3D.autoRotate = false;
        self.view3D.lastX = e.clientX;
        self.view3D.lastY = e.clientY;
      };
      window.addEventListener('mouseup', function() {
        self.view3D.dragging = false;
      });
      window.addEventListener('mousemove', function(e) {
        if (!self.view3D.dragging) return;
        var dx = e.clientX - self.view3D.lastX;
        var dy = e.clientY - self.view3D.lastY;
        self.view3D.lastX = e.clientX;
        self.view3D.lastY = e.clientY;
        self.view3D.ry += dx * 0.011;
        self.view3D.rx = Math.max(-1.35, Math.min(1.35, self.view3D.rx + dy * 0.011));
      });

      canvas.ontouchstart = function(e) {
        if (e.touches.length === 1) {
          self.view3D.dragging = true;
          self.view3D.autoRotate = false;
          self.view3D.lastX = e.touches[0].clientX;
          self.view3D.lastY = e.touches[0].clientY;
        }
      };
      canvas.ontouchmove = function(e) {
        if (!self.view3D.dragging || e.touches.length !== 1) return;
        e.preventDefault();
        var dx = e.touches[0].clientX - self.view3D.lastX;
        var dy = e.touches[0].clientY - self.view3D.lastY;
        self.view3D.lastX = e.touches[0].clientX;
        self.view3D.lastY = e.touches[0].clientY;
        self.view3D.ry += dx * 0.012;
        self.view3D.rx = Math.max(-1.35, Math.min(1.35, self.view3D.rx + dy * 0.012));
      };
      canvas.ontouchend = function() {
        self.view3D.dragging = false;
      };

      canvas.onwheel = function(e) {
        e.preventDefault();
        var delta = e.deltaY > 0 ? -0.08 : 0.08;
        self.view3D.zoom = Math.max(0.65, Math.min(1.75, self.view3D.zoom + delta));
      };

      // Galaxy 모드에서 3D 대륙 행성 클릭 시 해당 대륙으로 즉시 점프
      canvas.onclick = function(e) {
        if (!self.view3D.galaxyMode || !self.view3D.nodeScreenCoords.length) return;
        var rect = canvas.getBoundingClientRect();
        var mx = (e.clientX - rect.left) * (canvas.width / rect.width);
        var my = (e.clientY - rect.top) * (canvas.height / rect.height);
        for (var i = 0; i < self.view3D.nodeScreenCoords.length; i++) {
          var nd = self.view3D.nodeScreenCoords[i];
          var dist = Math.hypot(mx - nd.x, my - nd.y);
          if (dist <= nd.r + 12) {
            self.selectWorld(nd.id);
            break;
          }
        }
      };

      if (this.view3D.animId) {
        cancelAnimationFrame(this.view3D.animId);
      }

      function loop() {
        var c = document.getElementById('matheduQuest3DCanvas');
        if (!c) return;
        self.view3D.time += 0.022;
        if (self.view3D.autoRotate && !self.view3D.dragging) {
          self.view3D.ry += 0.0085;
        }
        self.drawMain3DScene(c);
        self.view3D.animId = requestAnimationFrame(loop);
      }
      loop();
    },

    drawMain3DScene: function(canvas) {
      var ctx = canvas.getContext('2d');
      var w = canvas.width;
      var h = canvas.height;
      var cx = w * 0.5;
      var cy = h * 0.52;
      var fov = Math.min(w, h) * 0.92;
      var camDist = 5.2;
      var v = this.view3D;
      var t = v.time;

      // 1. 3대 비주얼 테마(cosmic / sanctuary / euclid) 연동 3D 홀로그램 배경 그라데이션
      var themeCfg = this.getThemeConfig(this.state.themeSkin);
      var bgGrad = ctx.createRadialGradient(cx, cy * 0.85, 10, cx, cy, Math.max(w, h) * 0.75);
      bgGrad.addColorStop(0, themeCfg.canvasBgStops[0]);
      bgGrad.addColorStop(0.55, themeCfg.canvasBgStops[1]);
      bgGrad.addColorStop(1, themeCfg.canvasBgStops[2]);
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, w, h);

      // 2. 3D 배경 별자리 파티클
      for (var si = 0; si < STAR_FIELD.length; si++) {
        var st = STAR_FIELD[si];
        var rSt = rotate3D(st.x, st.y, st.z, v.rx * 0.4, v.ry * 0.4, 0);
        var pSt = project3D(rSt, cx, cy, fov, camDist + 2, 1.0);
        var twinkle = st.alpha * (0.65 + 0.35 * Math.sin(t * 2 + si));
        ctx.fillStyle = 'rgba(186,230,253,' + twinkle.toFixed(2) + ')';
        ctx.beginPath();
        ctx.arc(pSt.x, pSt.y, st.size, 0, Math.PI * 2);
        ctx.fill();
      }

      // 3. 3D 바닥 좌표 격자 평면 (z_plane in 3D = y = -1.55)
      ctx.lineWidth = 1;
      for (var gx = -2.4; gx <= 2.41; gx += 0.6) {
        var pA = project3D(rotate3D(gx, -1.55, -2.4, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
        var pB = project3D(rotate3D(gx, -1.55, 2.4, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
        ctx.strokeStyle = Math.abs(gx) < 0.01 ? themeCfg.gridHighlight : themeCfg.gridBase;
        ctx.beginPath();
        ctx.moveTo(pA.x, pA.y);
        ctx.lineTo(pB.x, pB.y);
        ctx.stroke();

        var pC = project3D(rotate3D(-2.4, -1.55, gx, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
        var pD = project3D(rotate3D(2.4, -1.55, gx, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
        ctx.beginPath();
        ctx.moveTo(pC.x, pC.y);
        ctx.lineTo(pD.x, pD.y);
        ctx.stroke();
      }

      // 3D 좌표축 (X, Y, Z) 표시 (X-Ray 보조선 모드 ON 시)
      if (v.showXray) {
        var axes = [
          { to: [2.2, 0, 0], col: 'rgba(248,113,113,0.65)', lbl: 'X축' },
          { to: [0, 1.9, 0], col: 'rgba(52,211,153,0.65)', lbl: 'Z(높이)축' },
          { to: [0, 0, 2.2], col: 'rgba(96,165,250,0.65)', lbl: 'Y축' }
        ];
        var origP = project3D(rotate3D(0, 0, 0, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
        for (var ai = 0; ai < axes.length; ai++) {
          var ax = axes[ai];
          var endP = project3D(rotate3D(ax.to[0], ax.to[1], ax.to[2], v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
          ctx.strokeStyle = ax.col;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(origP.x, origP.y);
          ctx.lineTo(endP.x, endP.y);
          ctx.stroke();
          ctx.fillStyle = ax.col;
          ctx.font = 'bold 11px sans-serif';
          ctx.fillText(ax.lbl, endP.x + 4, endP.y + 3);
        }
      }

      function proj(x, y, z) {
        return project3D(rotate3D(x, y, z, v.rx, v.ry, 0), cx, cy, fov, camDist, v.zoom);
      }

      // 4. Galaxy 전체 행성계 성좌 모드 vs 개별 대륙 3D 수학 모뉴먼트 모드
      if (v.galaxyMode) {
        this.drawGalaxyConstellation3D(ctx, proj, t);
        return;
      }

      var wid = this.state.activeWorldId || 'w1';
      if (wid === 'w1') {
        this.drawMonumentW1_Paraboloid(ctx, proj, t, v.showXray);
      } else if (wid === 'w2') {
        this.drawMonumentW2_TrigHelix(ctx, proj, t, v.showXray);
      } else if (wid === 'w3') {
        this.drawMonumentW3_RiemannCalculus(ctx, proj, t, v.showXray);
      } else if (wid === 'w4') {
        this.drawMonumentW4_DandelinSpheres(ctx, proj, t, v.showXray);
      } else if (wid === 'w5') {
        this.drawMonumentW5_TorusKnot(ctx, proj, t, v.showXray);
      } else {
        this.drawMonumentW6_CrownPolyhedra(ctx, proj, t, v.showXray);
      }

      // 5. 🔥 FEVER RUSH (3연속 콤보 달성 시 3D 황금 피버 링 오라)
      if ((this.state.combo || 0) >= 3) {
        ctx.strokeStyle = 'rgba(251,191,36,' + (0.65 + 0.3 * Math.sin(t * 5)).toFixed(2) + ')';
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        for (var fa = 0; fa <= 48; fa++) {
          var fTh = (fa / 48) * Math.PI * 2;
          var fRad = 1.92 + 0.08 * Math.sin(t * 4 + fa);
          var fPt = proj(fRad * Math.cos(fTh + t), 0.15 * Math.sin(fTh * 3 + t * 2), fRad * Math.sin(fTh + t));
          if (fa === 0) ctx.moveTo(fPt.x, fPt.y);
          else ctx.lineTo(fPt.x, fPt.y);
        }
        ctx.stroke();
      }
    },

    // 🌌 6대 대륙 3D 행성계 성좌 뷰
    drawGalaxyConstellation3D: function(ctx, proj, t) {
      var coords = [];
      var pts3D = [
        { w: WORLDS[0], x: -2.1, y: -0.7, z: 0.9, col: '#34d399' },
        { w: WORLDS[1], x: -1.1, y: -0.2, z: -1.1, col: '#fb923c' },
        { w: WORLDS[2], x: -0.1, y: 0.35, z: 1.1, col: '#38bdf8' },
        { w: WORLDS[3], x: 0.95, y: 0.55, z: -0.9, col: '#a78bfa' },
        { w: WORLDS[4], x: 1.75, y: 0.85, z: 0.7, col: '#f43f5e' },
        { w: WORLDS[5], x: 0.15, y: 1.35, z: 0.0, col: '#fbbf24' }
      ];

      // 궤도 연결선
      ctx.lineWidth = 2;
      ctx.strokeStyle = 'rgba(56,189,248,0.5)';
      ctx.beginPath();
      for (var i = 0; i < pts3D.length; i++) {
        var nd = pts3D[i];
        var p = proj(nd.x, nd.y + 0.1 * Math.sin(t * 2 + i), nd.z);
        coords.push({ id: nd.w.id, w: nd.w, x: p.x, y: p.y, z: p.z, r: Math.max(14, 78 / p.z), col: nd.col });
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();

      this.view3D.nodeScreenCoords = coords;

      // 노드 구체 및 라벨 렌더링
      for (var j = 0; j < coords.length; j++) {
        var c = coords[j];
        var isAct = (c.id === this.state.activeWorldId);
        var grad = ctx.createRadialGradient(c.x - c.r * 0.3, c.y - c.r * 0.3, 2, c.x, c.y, c.r * 1.4);
        grad.addColorStop(0, '#ffffff');
        grad.addColorStop(0.45, c.col);
        grad.addColorStop(1, 'rgba(15,23,42,0.1)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2);
        ctx.fill();

        if (isAct) {
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(c.x, c.y, c.r + 5 + 2 * Math.sin(t * 4), 0, Math.PI * 2);
          ctx.stroke();
        }

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('W' + c.w.num + ' ' + c.w.icon, c.x, c.y + 4);
        ctx.font = 'bold 11px sans-serif';
        ctx.fillStyle = '#e0f2fe';
        ctx.fillText(c.w.name.replace(/^제\d대륙\s*·\s*/, ''), c.x, c.y + c.r + 15);
      }
      ctx.textAlign = 'left';
    },

    // 🌱 World 1: 3D 회전 포물면 & 원과 직선의 정사영 타워
    drawMonumentW1_Paraboloid: function(ctx, proj, t, xray) {
      // 1. 포물면 y_3d = 0.55*(x^2 + z^2) - 0.9
      var rings = [0.45, 0.85, 1.25, 1.6];
      for (var ri = 0; ri < rings.length; ri++) {
        var r = rings[ri];
        var yH = 0.52 * r * r - 0.85;
        ctx.strokeStyle = 'rgba(52,211,153,' + (0.35 + ri * 0.14) + ')';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        for (var a = 0; a <= 48; a++) {
          var th = (a / 48) * Math.PI * 2;
          var p = proj(r * Math.cos(th), yH, r * Math.sin(th));
          if (a === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();

        // 바닥 평면(y = -1.55)에 정사영된 동심원 (원의 방정식 x^2 + y^2 = r^2)
        if (xray && ri === 2) {
          ctx.strokeStyle = 'rgba(56,189,248,0.85)';
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          for (var b = 0; b <= 48; b++) {
            var th2 = (b / 48) * Math.PI * 2;
            var p2 = proj(r * Math.cos(th2), -1.55, r * Math.sin(th2));
            if (b === 0) ctx.moveTo(p2.x, p2.y);
            else ctx.lineTo(p2.x, p2.y);
          }
          ctx.stroke();
        }
      }

      // 포물선 자오선 리브
      for (var m = 0; m < 12; m++) {
        var phi = (m / 12) * Math.PI * 2 + t * 0.3;
        ctx.strokeStyle = 'rgba(110,231,183,0.42)';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        for (var u = 0; u <= 20; u++) {
          var ru = (u / 20) * 1.6;
          var yu = 0.52 * ru * ru - 0.85;
          var pm = proj(ru * Math.cos(phi), yu, ru * Math.sin(phi));
          if (u === 0) ctx.moveTo(pm.x, pm.y);
          else ctx.lineTo(pm.x, pm.y);
        }
        ctx.stroke();
      }

      // 바닥 정사영 원과 움직이는 직선 (할선 <-> 접선 d = r)
      if (xray) {
        var rTarget = 1.25;
        var dLine = rTarget + 0.35 * Math.sin(t * 1.8);
        var isTangent = Math.abs(dLine - rTarget) < 0.09;
        var lP1 = proj(-1.8, -1.55, dLine);
        var lP2 = proj(1.8, -1.55, dLine);
        ctx.strokeStyle = isTangent ? '#fbbf24' : '#f472b6';
        ctx.lineWidth = isTangent ? 3.2 : 2.0;
        ctx.beginPath();
        ctx.moveTo(lP1.x, lP1.y);
        ctx.lineTo(lP2.x, lP2.y);
        ctx.stroke();

        // 원의 중심에서 직선에 내린 수선의 발 (거리 d)
        var cP = proj(0, -1.55, 0);
        var hP = proj(0, -1.55, dLine);
        ctx.strokeStyle = '#fbbf24';
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        ctx.moveTo(cP.x, cP.y);
        ctx.lineTo(hP.x, hP.y);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#fde047';
        ctx.beginPath();
        ctx.arc(hP.x, hP.y, isTangent ? 6 : 4, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    // 🔥 World 2: 3D 단위원 삼각함수 나선 & 지수·로그 대칭 쌍날개
    drawMonumentW2_TrigHelix: function(ctx, proj, t, xray) {
      var N = 110;
      var R = 1.15;
      // 1. 3D 삼각함수 나선 (R cos s, s, R sin s)
      ctx.strokeStyle = '#fb923c';
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (var i = 0; i <= N; i++) {
        var u = (i / N) * Math.PI * 4 - Math.PI * 2;
        var x = R * Math.cos(u + t * 1.5);
        var z = R * Math.sin(u + t * 1.5);
        var y = u * 0.24;
        var p = proj(x, y, z);
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();

      // 2. X-Ray 보조선: 뒷벽 정사영 사인파 y = sin(t) & 바닥 단위원 x^2 + z^2 = R^2
      if (xray) {
        ctx.strokeStyle = 'rgba(56,189,248,0.65)';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        for (var j = 0; j <= N; j++) {
          var u2 = (j / N) * Math.PI * 4 - Math.PI * 2;
          var x2 = R * Math.cos(u2 + t * 1.5);
          var y2 = u2 * 0.24;
          var pProj = proj(x2, y2, -1.85);
          if (j === 0) ctx.moveTo(pProj.x, pProj.y);
          else ctx.lineTo(pProj.x, pProj.y);
        }
        ctx.stroke();

        // 현재 위상 점과 정사영 연결선
        var curX = R * Math.cos(t * 1.5);
        var curZ = R * Math.sin(t * 1.5);
        var pCur = proj(curX, 0, curZ);
        var pFloor = proj(curX, -1.55, curZ);
        var pWall = proj(curX, 0, -1.85);

        ctx.strokeStyle = 'rgba(250,204,21,0.75)';
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        ctx.moveTo(pCur.x, pCur.y);
        ctx.lineTo(pFloor.x, pFloor.y);
        ctx.moveTo(pCur.x, pCur.y);
        ctx.lineTo(pWall.x, pWall.y);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#facc15';
        ctx.beginPath();
        ctx.arc(pCur.x, pCur.y, 6, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    // ⚡ World 3: 3D 구분구적법 리만 원판 적층 & 삼차함수 극값 곡면
    drawMonumentW3_RiemannCalculus: function(ctx, proj, t, xray) {
      // 1. 구분구적법 리만 원기둥 단면 적층
      var slices = 9;
      for (var s = 0; s < slices; s++) {
        var yBot = -1.25 + (s / slices) * 2.3;
        var rSlice = 0.65 + 0.55 * Math.sin((s / slices) * Math.PI + t * 0.8);
        ctx.strokeStyle = 'rgba(56,189,248,' + (0.35 + (s / slices) * 0.5) + ')';
        ctx.fillStyle = 'rgba(14,165,233,0.12)';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        for (var a = 0; a <= 36; a++) {
          var th = (a / 36) * Math.PI * 2;
          var p = proj(rSlice * Math.cos(th), yBot, rSlice * Math.sin(th));
          if (a === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }

      // 2. 삼차함수 극대·극소 3D 황금 궤도 곡선 y = 1/3 x^3 - x
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 3.2;
      ctx.beginPath();
      for (var k = -30; k <= 30; k++) {
        var xv = (k / 30) * 1.85;
        var yv = (1 / 3) * xv * xv * xv - xv;
        var p3 = proj(xv, yv, 0);
        if (k === -30) ctx.moveTo(p3.x, p3.y);
        else ctx.lineTo(p3.x, p3.y);
      }
      ctx.stroke();

      // 3. X-Ray: 움직이는 접선 (순간변화율 f'(x) = x^2 - 1)
      if (xray) {
        var x0 = 1.45 * Math.sin(t * 1.1);
        var y0 = (1 / 3) * x0 * x0 * x0 - x0;
        var slope = x0 * x0 - 1;
        var pt0 = proj(x0, y0, 0);
        var ptA = proj(x0 - 0.7, y0 - slope * 0.7, 0);
        var ptB = proj(x0 + 0.7, y0 + slope * 0.7, 0);

        ctx.strokeStyle = '#34d399';
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        ctx.moveTo(ptA.x, ptA.y);
        ctx.lineTo(ptB.x, ptB.y);
        ctx.stroke();

        ctx.fillStyle = '#10b981';
        ctx.beginPath();
        ctx.arc(pt0.x, pt0.y, 6, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    // 🔮 World 4: 단델린의 구(Dandelin Spheres) & 이중 원뿔곡선 3D 홀로그램
    drawMonumentW4_DandelinSpheres: function(ctx, proj, t, xray) {
      var kCone = 0.78;
      // 1. 이중 원뿔 (Double Cone) 모선 및 수평 원
      var heights = [-1.45, -1.0, -0.5, 0, 0.5, 1.0, 1.45];
      for (var hi = 0; hi < heights.length; hi++) {
        var yh = heights[hi];
        var rh = Math.abs(yh) * kCone;
        if (rh < 0.02) continue;
        ctx.strokeStyle = 'rgba(167,139,250,0.42)';
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        for (var a = 0; a <= 40; a++) {
          var th = (a / 40) * Math.PI * 2;
          var p = proj(rh * Math.cos(th), yh, rh * Math.sin(th));
          if (a === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
      }

      // 원뿔 모선 12개
      for (var m = 0; m < 12; m++) {
        var ang = (m / 12) * Math.PI * 2;
        var pTop = proj(1.45 * kCone * Math.cos(ang), 1.45, 1.45 * kCone * Math.sin(ang));
        var pBot = proj(1.45 * kCone * Math.cos(ang + Math.PI), -1.45, 1.45 * kCone * Math.sin(ang + Math.PI));
        ctx.strokeStyle = 'rgba(196,181,253,0.3)';
        ctx.lineWidth = 1.1;
        ctx.beginPath();
        ctx.moveTo(pTop.x, pTop.y);
        ctx.lineTo(pBot.x, pBot.y);
        ctx.stroke();
      }

      // 2. 단델린의 내접구 2개 (상단 내접구 S1, 하단 내접구 S2)
      var spheres = [
        { yc: 0.78, r: 0.48, col: 'rgba(251,191,36,0.85)' },
        { yc: -0.78, r: 0.48, col: 'rgba(56,189,248,0.85)' }
      ];
      for (var si = 0; si < spheres.length; si++) {
        var sp = spheres[si];
        var cSp = proj(0, sp.yc, 0);
        var edgeSp = proj(sp.r, sp.yc, 0);
        var radPx = Math.max(8, Math.hypot(edgeSp.x - cSp.x, edgeSp.y - cSp.y));
        var sGrad = ctx.createRadialGradient(cSp.x - radPx * 0.3, cSp.y - radPx * 0.3, 2, cSp.x, cSp.y, radPx);
        sGrad.addColorStop(0, '#ffffff');
        sGrad.addColorStop(0.5, sp.col);
        sGrad.addColorStop(1, 'rgba(15,23,42,0.15)');
        ctx.fillStyle = sGrad;
        ctx.beginPath();
        ctx.arc(cSp.x, cSp.y, radPx, 0, Math.PI * 2);
        ctx.fill();
      }

      // 3. 비스듬한 절단 평면이 만드는 타원(Ellipse) & 초점 F1, F2
      if (xray) {
        ctx.strokeStyle = '#34d399';
        ctx.lineWidth = 3;
        ctx.beginPath();
        for (var e = 0; e <= 48; e++) {
          var thE = (e / 48) * Math.PI * 2;
          var ex = 0.72 * Math.cos(thE);
          var ez = 0.58 * Math.sin(thE);
          var ey = 0.62 + 0.28 * ex;
          var pe = proj(ex, ey, ez);
          if (e === 0) ctx.moveTo(pe.x, pe.y);
          else ctx.lineTo(pe.x, pe.y);
        }
        ctx.stroke();

        // 타원의 두 초점 F1, F2 강조
        var f1 = proj(-0.35, 0.52, 0);
        var f2 = proj(0.35, 0.72, 0);
        ctx.fillStyle = '#fde047';
        ctx.beginPath();
        ctx.arc(f1.x, f1.y, 5, 0, Math.PI * 2);
        ctx.arc(f2.x, f2.y, 5, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    // 🐉 World 5: 3D (2,3)-토러스 매듭 & Frenet-Serret 벡터장 요새
    drawMonumentW5_TorusKnot: function(ctx, proj, t, xray) {
      var N = 150;
      var pK = 2, qK = 3;
      var R = 1.05, a = 0.42;

      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 3.2;
      ctx.beginPath();
      for (var i = 0; i <= N; i++) {
        var u = (i / N) * Math.PI * 2;
        var r = R + a * Math.cos(qK * u + t);
        var x = r * Math.cos(pK * u);
        var z = r * Math.sin(pK * u);
        var y = a * Math.sin(qK * u + t);
        var pt = proj(x, y, z);
        if (i === 0) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
      }
      ctx.stroke();

      // X-Ray: 궤도를 주행하는 Frenet-Serret 3축 벡터 (접선 T, 법선 N)
      if (xray) {
        var u0 = (t * 0.7) % (Math.PI * 2);
        var r0 = R + a * Math.cos(qK * u0 + t);
        var x0 = r0 * Math.cos(pK * u0);
        var z0 = r0 * Math.sin(pK * u0);
        var y0 = a * Math.sin(qK * u0 + t);

        var p0 = proj(x0, y0, z0);
        var pCenter = proj(0, 0, 0);

        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(pCenter.x, pCenter.y);
        ctx.lineTo(p0.x, p0.y);
        ctx.stroke();

        ctx.fillStyle = '#fbbf24';
        ctx.beginPath();
        ctx.arc(p0.x, p0.y, 6.5, 0, Math.PI * 2);
        ctx.fill();
      }
    },

    // 👑 World 6: 황금비 정이십면체 왕관 & 30문항 피보나치 구면 성좌
    drawMonumentW6_CrownPolyhedra: function(ctx, proj, t, xray) {
      var scalePoly = 0.72;
      // 1. 정이십면체 30개 모서리
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 2.2;
      for (var ei = 0; ei < ICOSA_EDGES.length; ei++) {
        var vA = ICOSA_VERTS[ICOSA_EDGES[ei][0]];
        var vB = ICOSA_VERTS[ICOSA_EDGES[ei][1]];
        var pA = proj(vA[0] * scalePoly, vA[1] * scalePoly, vA[2] * scalePoly);
        var pB = proj(vB[0] * scalePoly, vB[1] * scalePoly, vB[2] * scalePoly);
        ctx.beginPath();
        ctx.moveTo(pA.x, pA.y);
        ctx.lineTo(pB.x, pB.y);
        ctx.stroke();
      }

      // 2. 외접하는 30개 수능 문항 피보나치 구면 별자리 노드
      if (xray) {
        var R_outer = 1.62;
        for (var i = 0; i < 30; i++) {
          var y = 1 - (2 * i + 1) / 30;
          var rad = Math.sqrt(Math.max(0, 1 - y * y));
          var theta = (2 * Math.PI * i) / PHI + t * 0.4;
          var x = rad * Math.cos(theta) * R_outer;
          var z = rad * Math.sin(theta) * R_outer;
          var pNode = proj(x, y * R_outer, z);

          ctx.fillStyle = (i === 21 || i === 29) ? '#f43f5e' : '#38bdf8';
          ctx.beginPath();
          ctx.arc(pNode.x, pNode.y, (i === 21 || i === 29) ? 4.5 : 3.0, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    },

    // =========================================================================
    // ⚔️ 3D 보스 배틀 아레나 (3중 짐벌 결계 링 파쇄 & 3D 파티클 폭발 엔진)
    // =========================================================================
    initBattle3DCanvas: function() {
      var self = this;
      if (this.battle3D.animId) {
        cancelAnimationFrame(this.battle3D.animId);
      }
      this.battle3D.particles = [];

      function loopBattle() {
        var c = document.getElementById('questBattle3DCanvas');
        if (!c) return;
        var speedMult = self.meditateMode ? 0.25 : 1.0;
        self.battle3D.time += 0.032 * speedMult;
        self.battle3D.ry += 0.018 * speedMult;
        if (self.battle3D.shake > 0) self.battle3D.shake *= 0.86;
        if (self.battle3D.laserTimer > 0) self.battle3D.laserTimer--;
        if (self.battle3D.shieldFlash > 0) self.battle3D.shieldFlash--;

        // 🧠 아르키메데스의 통찰력 축적 게이지 실시간 자연 충전 (사색 모드 / 아르키메데스 성물 가속)
        if ((self.insightGauge || 0) < 100) {
          var rate = 0.095;
          if (self.hasRelic('relic_archimedes')) rate *= 2.0;
          if (self.meditateMode) rate *= 1.85;
          self.insightGauge = Math.min(100, (self.insightGauge || 0) + rate);
          self.updateInsightGaugeDOM();
        }
        // 🧘 사색 모드 중에는 기하 통찰 필살기 게이지도 자연 충전
        if (self.meditateMode && (self.state.ultimateGauge || 0) < 100) {
          self.state.ultimateGauge = Math.min(100, (self.state.ultimateGauge || 0) + 0.04);
        }

        self.drawBattle3DArena(c);
        self.battle3D.animId = requestAnimationFrame(loopBattle);
      }
      loopBattle();
    },

    spawnRingShatterParticles: function(colorStr) {
      for (var i = 0; i < 48; i++) {
        var ang = Math.random() * Math.PI * 2;
        var elev = (Math.random() - 0.5) * Math.PI;
        var spd = 0.04 + Math.random() * 0.09;
        this.battle3D.particles.push({
          x: Math.cos(ang) * 1.1,
          y: Math.sin(elev) * 0.6,
          z: Math.sin(ang) * 1.1,
          vx: Math.cos(ang) * spd,
          vy: Math.sin(elev) * spd,
          vz: Math.sin(ang) * spd,
          life: 1.0,
          col: colorStr
        });
      }
      this.battle3D.shake = 12;
      this.battle3D.laserTimer = 18;
    },

    drawBattle3DArena: function(canvas) {
      var ctx = canvas.getContext('2d');
      var w = canvas.width;
      var h = canvas.height;
      var b = this.battle3D;
      var shakeX = (Math.random() - 0.5) * b.shake;
      var shakeY = (Math.random() - 0.5) * b.shake;
      var cx = w * 0.5 + shakeX;
      var cy = h * 0.52 + shakeY;
      var fov = Math.min(w, h) * 1.05;
      var camDist = 4.6;

      // 배경 (3대 비주얼 테마 & 사색 모드 연동)
      var themeCfg = this.getThemeConfig(this.state.themeSkin);
      var grad = ctx.createRadialGradient(cx, cy, 8, cx, cy, w * 0.65);
      grad.addColorStop(0, this.meditateMode ? '#2e1065' : themeCfg.battleBgStops[0]);
      grad.addColorStop(0.6, this.meditateMode ? '#171238' : themeCfg.battleBgStops[1]);
      grad.addColorStop(1, this.meditateMode ? '#09071a' : themeCfg.battleBgStops[2]);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      var stg = this.activeStage;
      var totalSteps = stg ? stg.steps.length : 3;
      var remainingRings = Math.max(0, totalSteps - this.activeStepIdx);

      // 1. 남아있는 3중 짐벌 수식 결계 링 (R1 Cyan, R2 Gold, R3 Crimson)
      var ringConfigs = [
        { rad: 1.48, rx: 0.45, rz: 0.3, col: '#38bdf8', spd: 1.2 },
        { rad: 1.22, rx: -0.7, rz: -0.4, col: '#fbbf24', spd: -1.5 },
        { rad: 0.96, rx: 1.1, rz: 0.5, col: '#f43f5e', spd: 1.9 }
      ];
      for (var ri = 0; ri < remainingRings && ri < ringConfigs.length; ri++) {
        var rc = ringConfigs[ri];
        ctx.strokeStyle = rc.col;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        for (var a = 0; a <= 44; a++) {
          var th = (a / 44) * Math.PI * 2;
          var pt = rotate3D(
            rc.rad * Math.cos(th),
            0,
            rc.rad * Math.sin(th),
            rc.rx + b.time * 0.4 * rc.spd,
            b.ry * rc.spd,
            rc.rz
          );
          var p2 = project3D(pt, cx, cy, fov, camDist, 1.0);
          if (a === 0) ctx.moveTo(p2.x, p2.y);
          else ctx.lineTo(p2.x, p2.y);
        }
        ctx.stroke();
      }

      // 2. 중앙 3D 보스 기하 코어 (회전 정이십면체 코어)
      var coreScale = 0.52;
      ctx.strokeStyle = remainingRings === 1 ? '#f43f5e' : '#a78bfa';
      ctx.lineWidth = 2.0;
      for (var ei = 0; ei < ICOSA_EDGES.length; ei++) {
        var vA = ICOSA_VERTS[ICOSA_EDGES[ei][0]];
        var vB = ICOSA_VERTS[ICOSA_EDGES[ei][1]];
        var rA = rotate3D(vA[0] * coreScale, vA[1] * coreScale, vA[2] * coreScale, b.time * 0.7, b.ry * 1.4, 0.3);
        var rB = rotate3D(vB[0] * coreScale, vB[1] * coreScale, vB[2] * coreScale, b.time * 0.7, b.ry * 1.4, 0.3);
        var pA = project3D(rA, cx, cy, fov, camDist, 1.0);
        var pB = project3D(rB, cx, cy, fov, camDist, 1.0);
        ctx.beginPath();
        ctx.moveTo(pA.x, pA.y);
        ctx.lineTo(pB.x, pB.y);
        ctx.stroke();
      }

      // 3. 정답 타격 시 레이저 빔 연출 및 🌟 기하 통찰 필살기 초신성 레이저 폭격 연출
      if (b.supernovaTimer && b.supernovaTimer > 0) {
        b.supernovaTimer--;
        ctx.strokeStyle = '#fde047';
        ctx.lineWidth = b.supernovaTimer * 0.55;
        ctx.beginPath();
        ctx.moveTo(0, 0); ctx.lineTo(cx, cy);
        ctx.moveTo(w, 0); ctx.lineTo(cx, cy);
        ctx.moveTo(0, h); ctx.lineTo(cx, cy);
        ctx.moveTo(w, h); ctx.lineTo(cx, cy);
        ctx.moveTo(cx, 0); ctx.lineTo(cx, h);
        ctx.stroke();
      }
      if (b.laserTimer > 0) {
        ctx.strokeStyle = '#34d399';
        ctx.lineWidth = b.laserTimer * 0.45;
        ctx.beginPath();
        ctx.moveTo(w * 0.12, h * 0.92);
        ctx.lineTo(cx, cy);
        ctx.moveTo(w * 0.88, h * 0.92);
        ctx.lineTo(cx, cy);
        ctx.stroke();
      }

      // 4. 오답 시 3D 육각형 허니컴 디딤돌 방어막 연출
      if (b.shieldFlash > 0) {
        ctx.strokeStyle = 'rgba(56,189,248,' + (b.shieldFlash / 25).toFixed(2) + ')';
        ctx.fillStyle = 'rgba(56,189,248,' + (b.shieldFlash / 80).toFixed(2) + ')';
        ctx.lineWidth = 3;
        ctx.beginPath();
        for (var hi = 0; hi <= 6; hi++) {
          var hAng = (hi / 6) * Math.PI * 2;
          var hx = cx + Math.cos(hAng) * 58;
          var hy = cy + Math.sin(hAng) * 58;
          if (hi === 0) ctx.moveTo(hx, hy);
          else ctx.lineTo(hx, hy);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }

      // 5. 결계 파쇄 3D 파티클 업데이트 및 렌더링
      for (var pi = b.particles.length - 1; pi >= 0; pi--) {
        var ptc = b.particles[pi];
        ptc.x += ptc.vx;
        ptc.y += ptc.vy;
        ptc.z += ptc.vz;
        ptc.life -= 0.028;
        if (ptc.life <= 0) {
          b.particles.splice(pi, 1);
          continue;
        }
        var pp = project3D(ptc, cx, cy, fov, camDist, 1.0);
        ctx.fillStyle = ptc.col;
        ctx.globalAlpha = Math.max(0, ptc.life);
        ctx.beginPath();
        ctx.arc(pp.x, pp.y, 3.5 * ptc.life, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
      }

      // 6. 🔥 FEVER RUSH (연속 콤보 피버 오라 링) 및 🧘 사색/유레카 파동 링
      var feverThresh = this.getFeverThreshold();
      if ((this.state.combo || 0) >= feverThresh) {
        ctx.strokeStyle = 'rgba(251,191,36,' + (0.7 + 0.3 * Math.sin(b.time * 6)).toFixed(2) + ')';
        ctx.lineWidth = 2.8;
        ctx.beginPath();
        for (var fa = 0; fa <= 40; fa++) {
          var fAng = (fa / 40) * Math.PI * 2;
          var fPt = rotate3D(1.68 * Math.cos(fAng), 0.18 * Math.sin(fAng * 4 + b.time * 3), 1.68 * Math.sin(fAng), 0.25, b.ry * 1.5, -0.2);
          var fP2 = project3D(fPt, cx, cy, fov, camDist, 1.0);
          if (fa === 0) ctx.moveTo(fP2.x, fP2.y);
          else ctx.lineTo(fP2.x, fP2.y);
        }
        ctx.stroke();
      }
      if (this.meditateMode || (this.insightGauge || 0) >= 90) {
        ctx.strokeStyle = (this.insightGauge >= 90) ? 'rgba(253,224,71,0.85)' : 'rgba(94,234,212,0.75)';
        ctx.lineWidth = 2.2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.arc(cx, cy, 62 + 4 * Math.sin(b.time * 4), 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // 7. 💥 ALL-OUT GEOMETRIC FINISH! — Q.E.D. (총공격 공간 절단 슬래시 연출)
      if (b.allOutSlashTimer && b.allOutSlashTimer > 0) {
        b.allOutSlashTimer--;
        ctx.save();
        ctx.strokeStyle = '#fde047';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(0, h * 0.85);
        ctx.lineTo(w, h * 0.15);
        ctx.moveTo(w * 0.15, 0);
        ctx.lineTo(w * 0.85, h);
        ctx.stroke();

        ctx.fillStyle = 'rgba(251,191,36,0.96)';
        ctx.font = '900 16px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('✨ ALL-OUT GEOMETRIC FINISH! — Q.E.D. ✨', cx, cy - 8);
        ctx.restore();
      }

      // 8. 💬 3D 플로팅 데미지 & 수학 판정 텍스트 (PART BREAK / CRITICAL DERIVATION! / DEEP EUREKA!! / Q.E.D.)
      if (b.floatingTexts && b.floatingTexts.length > 0) {
        for (var fi = b.floatingTexts.length - 1; fi >= 0; fi--) {
          var ft = b.floatingTexts[fi];
          ft.y += ft.vy;
          ft.life -= 0.022;
          if (ft.life <= 0) {
            b.floatingTexts.splice(fi, 1);
            continue;
          }
          ctx.save();
          ctx.globalAlpha = Math.max(0, Math.min(1, ft.life));
          ctx.font = '900 13px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillStyle = '#020617';
          ctx.fillText(ft.text, cx + ft.x + 1, cy + ft.y + 1);
          ctx.fillStyle = ft.color || '#fde047';
          ctx.fillText(ft.text, cx + ft.x, cy + ft.y);
          ctx.restore();
        }
      }
    },

    startStageBattle: function(stageObj) {
      if (!stageObj) return;
      this.activeStage = stageObj;
      this.activeStepIdx = 0;
      this.stepStartTime = Date.now();
      this.stepAttempts = 0;
      this.stageMistakes = 0;
      this.eulerShieldUsed = false;
      this.scratchpadOpen = false;
      this.resetStepContemplation();

      // 👑 가우스의 등차수열 왕관: 전투 개시 시 기본 1콤보 부여
      if (this.hasRelic('relic_gauss') && (this.state.combo || 0) < 1) {
        this.state.combo = 1;
      }
      // 🔮 단델린의 쌍구면 렌즈: 3D 보조선 투시 상시 활성화
      if (this.hasRelic('relic_dandelin')) {
        this.view3D.showXray = true;
      }
      // 🌟 성좌 [직관의 눈 ★1]: 전투 개시 시 필살기 게이지 최소 20% 보장
      if (this.hasConstellationStar('c2_s1') && (this.state.ultimateGauge || 0) < 20) {
        this.state.ultimateGauge = 20;
      }
      // 🌟 성좌 [귀납의 방패 ★1]: 전투 개시 시 보호막 100% 완충
      if (this.hasConstellationStar('c3_s1')) {
        this.state.shieldHp = 100;
      }
      saveQuestState(this.state);
      this.renderBattleModal();
    },

    startStageById: function(worldId, stageId) {
      var w = this.getWorldById(worldId);
      if (!w) return;
      for (var i = 0; i < w.stages.length; i++) {
        if (w.stages[i].id === stageId) {
          this.playGameSfx('summon');
          this.startStageBattle(w.stages[i]);
          return;
        }
      }
    },

    // ⚡ 오답 약점 3D 리벤지 보스 소환 (`MatheduGame.getWrongAnswers()` 우선 연동)
    summonWeaknessRevengeBoss: function(worldId) {
      var self = this;
      this.playGameSfx('summon');
      this.state.dailyQuests = ensureDailyQuests(this.state.dailyQuests);
      this.state.dailyQuests.archiveSummoned = (this.state.dailyQuests.archiveSummoned || 0) + 1;
      saveQuestState(this.state);

      var wrongList = (window.MatheduGame && typeof window.MatheduGame.getWrongAnswers === 'function')
        ? window.MatheduGame.getWrongAnswers()
        : [];

      if (wrongList && wrongList.length > 0) {
        var targetWrong = wrongList[Math.floor(Math.random() * wrongList.length)];
        var targetSlug = targetWrong.slug;

        // 1) WORLDS 내 모든 스테이지 중 해당 slug와 일치하는 보스가 있는지 탐색
        for (var wi = 0; wi < WORLDS.length; wi++) {
          var stgs = WORLDS[wi].stages || [];
          for (var si = 0; si < stgs.length; si++) {
            if (stgs[si].slug === targetSlug || stgs[si].id === targetSlug) {
              var revengeStage = JSON.parse(JSON.stringify(stgs[si]));
              revengeStage.gradeBadge = '⚡ 약점 3D 리벤지 레이드 · ' + revengeStage.gradeBadge;
              revengeStage.bossName = '🔥 [약점 복수전] ' + revengeStage.bossName;
              revengeStage.xpReward = Math.round((revengeStage.xpReward || 60) * 1.5);
              self.startStageBattle(revengeStage);
              return;
            }
          }
        }
      }

      // 2) 오답 문항이 없거나 샤드 기출 문항인 경우 현재 대륙의 기출 보스를 소환
      this.summonRandomArchiveProblem(worldId || this.state.activeWorldId);
    },

    // 16,548문항 연도별 샤드 DB에서 실시간으로 해당 대륙 기출 보스 소환!
    summonRandomArchiveProblem: function(worldId) {
      var self = this;
      this.playGameSfx('summon');
      this.state.dailyQuests = ensureDailyQuests(this.state.dailyQuests);
      this.state.dailyQuests.archiveSummoned = (this.state.dailyQuests.archiveSummoned || 0) + 1;
      saveQuestState(this.state);
      var w = this.getWorldById(worldId || this.state.activeWorldId);
      var years = w.shardYears || ['2025'];
      var pickYear = years[Math.floor(Math.random() * years.length)];
      var basePath = window.location.pathname.indexOf('/board/') !== -1 ? 'archive_shards/' : 'board/archive_shards/';
      var shardUrl = basePath + 'exam_' + pickYear + '.json';

      var btn = document.getElementById('btnSummonArchiveBoss');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '⏳ 16,548문항 아카이브에서 맞춤형 3D 기출 보스 소환 중...';
      }

      function buildStageFromShardProb(prob) {
        var unitParts = prob.unit_parts || [];
        var leafUnit = unitParts.length ? unitParts[unitParts.length - 1] : w.name;
        var opts = prob.options || ['$1$', '$2$', '$3$', '$4$', '$5$'];
        var ansIdx = parseInt(prob.answer || 1, 10);
        var ansDisplay = opts[ansIdx - 1] || String(ansIdx);

        var s3Q = prob.s3_q || {
          stem: '출발 조건을 <b>' + leafUnit + '</b>의 수식으로 세울 때 올바른 식은?<br>' + (prob.s3 || ''),
          options: opts,
          answer: ansIdx,
          exp: prob.s3 || '주어진 조건을 수식으로 나타냅니다.'
        };
        var s4Q = prob.s4_q || {
          stem: '중간 관계식을 정리하여 계산할 때 알맞은 식은?<br>' + (prob.s4 || ''),
          options: opts,
          answer: ansIdx,
          exp: prob.s4 || '관계식을 정리합니다.'
        };

        var dynamicStage = {
          id: 'dyn_' + prob.slug,
          slug: prob.slug,
          url: (prob.standaloneSlug ? ('board/' + prob.standaloneSlug + '.html') : ('board/archive.html?id=' + encodeURIComponent(prob.slug))),
          gradeBadge: '🎲 실시간 3D 기출 소환 · ' + prob.examYear + '학년도 ' + prob.month + ' ' + prob.grade + ' ' + prob.subject + ' ' + prob.qNum + '번 (' + (prob.point || '3') + '점)',
          bossName: '👾 [' + leafUnit + '] ' + prob.title.replace(/^\[.*?\]\s*/, ''),
          scoreReward: parseInt(prob.point || '3', 10),
          xpReward: 50,
          symbols: [
            { sym: '📌 핵심 단원: ' + leafUnit, desc: (prob.intent || (leafUnit + '의 정의와 성질을 적용하는 실전 기출문항입니다.')) },
            { sym: '🎯 배점 및 번호: ' + prob.qNum + '번 (' + (prob.point || '3') + '점)', desc: '초등 디딤돌부터 출발 식(가) ➔ 중간 유도식(나) ➔ 본문항 순서로 3중 결계를 격파하세요!' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🌱 1단계 · [외곽 결계 파쇄: 출발 조건 식 (가)] ' + leafUnit,
              know: '문제의 출발 조건을 수식으로 옮기는 첫 디딤돌입니다.<br>• <b>핵심 단서</b>: ' + (prob.s3 || leafUnit),
              stem: s3Q.stem,
              options: s3Q.options,
              answer: s3Q.answer,
              exp: s3Q.exp
            },
            {
              stepNum: 2,
              label: '🌳 2단계 · [중간 결계 파쇄: 관계식 유도 (나)] ' + leafUnit,
              know: '출발 식을 변형하여 목표값에 다가가는 중간 유도 단계입니다.<br>• <b>핵심 전개</b>: ' + (prob.s4 || leafUnit),
              stem: s4Q.stem,
              options: s4Q.options,
              answer: s4Q.answer,
              exp: s4Q.exp
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [보스 코어 격파: 실전 기출 본문항] ' + prob.examYear + '학년도 ' + prob.qNum + '번',
              know: '1~2단계의 유도 결과를 결합하여 최종 정답을 도출합니다.',
              stem: prob.stem,
              options: opts,
              answer: ansIdx,
              exp: '<b>[공식 풀이 요약]</b><br>' + ((prob.exp_lines && prob.exp_lines.length) ? prob.exp_lines.slice(0, 6).join('<br>') : ('정답은 ' + ansDisplay + '입니다.'))
            }
          ]
        };

        self.state.summonedCount = (self.state.summonedCount || 0) + 1;
        saveQuestState(self.state);
        self.startStageBattle(dynamicStage);
      }

      function pickFromShardData(data) {
        var probsObj = (data && data.problems) ? data.problems : {};
        var keys = Object.keys(probsObj);
        var matches = [];
        for (var i = 0; i < keys.length; i++) {
          var p = probsObj[keys[i]];
          var hay = ((p.title || '') + ' ' + (p.subject || '') + ' ' + (p.unit_parts || []).join(' ')).toLowerCase();
          var kwMatch = false;
          for (var k = 0; k < w.shardKeywords.length; k++) {
            if (hay.indexOf(w.shardKeywords[k].toLowerCase()) !== -1) {
              kwMatch = true;
              break;
            }
          }
          if (kwMatch) matches.push(p);
        }
        var pool = matches.length > 0 ? matches : keys.map(function(k) { return probsObj[k]; });
        if (pool.length === 0) return;
        var chosen = pool[Math.floor(Math.random() * pool.length)];
        buildStageFromShardProb(chosen);
      }

      if (this.shardCache[pickYear]) {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '🎲 이 대륙의 3D 기출 보스 무작위 소환 (16,548문항 DB)';
        }
        pickFromShardData(this.shardCache[pickYear]);
        return;
      }

      fetch(shardUrl)
        .then(function(r) { return r.json(); })
        .then(function(data) {
          self.shardCache[pickYear] = data;
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🎲 이 대륙의 3D 기출 보스 무작위 소환 (16,548문항 DB)';
          }
          pickFromShardData(data);
        })
        .catch(function() {
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🎲 이 대륙의 3D 기출 보스 무작위 소환 (16,548문항 DB)';
          }
          if (w.stages && w.stages.length) {
            self.startStageBattle(w.stages[0]);
          }
        });
    },

    summonMin7014Grimoire: function(url) {
      this.state.shieldHp = 100;
      this.state.ultimateGauge = Math.min(100, (this.state.ultimateGauge || 0) + 50);
      this.state.dailyQuests = ensureDailyQuests(this.state.dailyQuests);
      this.state.dailyQuests.grimoireOpened = (this.state.dailyQuests.grimoireOpened || 0) + 1;
      saveQuestState(this.state);
      this.playGameSfx('hit');
      if (window.MatheduGame && typeof window.MatheduGame.unlockBadge === 'function') {
        window.MatheduGame.unlockBadge('min7014_explorer');
        window.MatheduGame.addXP(15, '📐 민은기 선생님 시각 증명 비급서 탐구 (+보호막 100% · 필살기 +50%)');
      }
      var hpEl = document.getElementById('questBattleShieldText');
      if (hpEl) hpEl.textContent = '100%';
      this.renderConsoleHub();
      if (url) {
        window.open(url, '_blank', 'noopener');
      }
    },

    // 🎁 오늘의 수능 만점 일일 퀘스트 3종 완료 보상 황금 보물상자 열기
    claimDailyTreasureChest: function() {
      var dq = ensureDailyQuests(this.state.dailyQuests);
      if (dq.chestClaimed) return;
      if (dq.stepsCleared < 3 || dq.archiveSummoned < 1 || dq.grimoireOpened < 1) return;

      dq.chestClaimed = true;
      this.state.dailyQuests = dq;
      this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + 5);
      this.state.shieldHp = 100;
      this.state.ultimateGauge = 100;
      saveQuestState(this.state);

      this.playGameSfx('victory');
      if (window.MatheduGame) {
        window.MatheduGame.addXP(100, '🎁 오늘의 수능 만점 일일 퀘스트 3종 올클리어 황금 보물상자! (+수능 5점)');
        if (typeof window.MatheduGame.fireConfetti === 'function') {
          window.MatheduGame.fireConfetti();
        }
      }
      this.renderConsoleHub();
    },

    // 🌟 [3D 보스 배틀 필살기 시스템: "기하학적 통찰의 일격 (Geometric Ultimate Strike)"]
    castGeometricUltimate: function() {
      var stg = this.activeStage;
      if (!stg) return;
      var curStep = stg.steps[this.activeStepIdx];
      if (!curStep) return;
      if ((this.state.ultimateGauge || 0) < 100) return;

      this.state.ultimateGauge = 0;
      saveQuestState(this.state);

      // 3D 초신성 레이저 폭격 & 황금 파티클 폭발 & 승리 팡파르
      this.battle3D.supernovaTimer = 34;
      this.spawnRingShatterParticles('#fde047');
      this.playGameSfx('victory');

      // 5지선다 중 오답 2개 즉시 소거 (취소선 + 비활성화)
      var ansIdx = parseInt(curStep.answer, 10);
      var wrongIndices = [];
      var totalOpts = (curStep.options || []).length;
      for (var i = 1; i <= totalOpts; i++) {
        if (i !== ansIdx) wrongIndices.push(i);
      }
      // 셔플 후 2개 선택
      wrongIndices.sort(function() { return Math.random() - 0.5; });
      var toEliminate = wrongIndices.slice(0, 2);

      var btns = document.querySelectorAll('.quest-battle-opt-btn');
      for (var b = 0; b < btns.length; b++) {
        var btnIdx = b + 1;
        if (toEliminate.indexOf(btnIdx) !== -1) {
          btns[b].disabled = true;
          btns[b].style.opacity = '0.38';
          btns[b].style.textDecoration = 'line-through';
          btns[b].style.background = '#f1f5f9';
          btns[b].style.borderColor = '#cbd5e1';
          btns[b].style.cursor = 'not-allowed';
        }
      }

      var ultBtn = document.getElementById('btnCastGeometricUltimate');
      if (ultBtn) {
        ultBtn.disabled = true;
        ultBtn.innerHTML = '🌟 기하 통찰의 일격 발동 완료! (오답 ' + toEliminate.join('번, ') + '번 소거됨)';
        ultBtn.style.background = '#64748b';
      }

      var ultBanner = document.getElementById('questUltimateInsightBox');
      if (ultBanner) {
        ultBanner.style.display = 'block';
        ultBanner.innerHTML =
          '🌟 <b>[기하 통찰 필살기 발동!]</b> 초신성 레이저가 함정 선택지 <b>' + toEliminate.join('번, ') + '번</b>을 분쇄했습니다!<br>' +
          '👩‍🏫 <b>mathteacher 결정적 단서:</b> ' + (curStep.exp || curStep.know);
        typesetMath(ultBanner);
      }
    },

    // =========================================================================
    // 🚀 [60초 3D 스피드 디딤돌 블리츠 (60s 3D Speed Blitz Mini-Game)]
    // =========================================================================
    blitzState: {
      active: false,
      timeLeft: 60,
      score: 0,
      combo: 0,
      qIdx: 0,
      pool: [],
      timerId: null,
      animId: null,
      warpTime: 0
    },

    startSpeedBlitzMode: function() {
      var self = this;
      this.playGameSfx('summon');
      var shuffled = SPEED_BLITZ_QUESTIONS.slice().sort(function() { return Math.random() - 0.5; });
      this.blitzState.active = true;
      this.blitzState.timeLeft = this.hasConstellationStar('c4_s3') ? 70 : 60;
      this.blitzState.score = 0;
      this.blitzState.combo = 0;
      this.blitzState.qIdx = 0;
      this.blitzState.pool = shuffled;

      if (this.blitzState.timerId) clearInterval(this.blitzState.timerId);
      this.renderSpeedBlitzModal();

      this.blitzState.timerId = setInterval(function() {
        if (!self.blitzState.active) return;
        if (self.meditateMode) {
          var tFreezeEl = document.getElementById('questBlitzTimerText');
          if (tFreezeEl) tFreezeEl.textContent = self.blitzState.timeLeft + '초 (🧘 사색 정지 중)';
          return;
        }
        self.blitzState.timeLeft--;
        var tEl = document.getElementById('questBlitzTimerText');
        if (tEl) tEl.textContent = self.blitzState.timeLeft + '초';
        if (self.blitzState.timeLeft <= 0) {
          self.finishSpeedBlitzMode();
        }
      }, 1000);
    },

    initBlitz3DCanvas: function() {
      var self = this;
      if (this.blitzState.animId) cancelAnimationFrame(this.blitzState.animId);

      function loopBlitz() {
        var c = document.getElementById('questBlitz3DCanvas');
        if (!c || !self.blitzState.active) return;
        var ctx = c.getContext('2d');
        var w = c.width, h = c.height;
        var cx = w * 0.5, cy = h * 0.5;
        self.blitzState.warpTime += 0.055 + Math.min(0.08, self.blitzState.combo * 0.01);
        var wt = self.blitzState.warpTime;

        ctx.fillStyle = '#040816';
        ctx.fillRect(0, 0, w, h);

        // 3D 하이퍼워프 광속 성운 라인
        for (var i = 0; i < 42; i++) {
          var ang = (i / 42) * Math.PI * 2 + wt * 0.15;
          var r1 = ((wt * 60 + i * 19) % 160) + 12;
          var r2 = r1 + 26 + self.blitzState.combo * 4;
          ctx.strokeStyle = (self.blitzState.combo >= 3) ? 'rgba(251,191,36,0.75)' : 'rgba(56,189,248,0.65)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(cx + Math.cos(ang) * r1, cy + Math.sin(ang) * (r1 * 0.45));
          ctx.lineTo(cx + Math.cos(ang) * r2, cy + Math.sin(ang) * (r2 * 0.45));
          ctx.stroke();
        }

        // 중앙 회전 황금 다면체 코어
        var fov = 140;
        ctx.strokeStyle = self.blitzState.combo >= 3 ? '#fbbf24' : '#34d399';
        ctx.lineWidth = 1.8;
        for (var ei = 0; ei < ICOSA_EDGES.length; ei++) {
          var vA = ICOSA_VERTS[ICOSA_EDGES[ei][0]];
          var vB = ICOSA_VERTS[ICOSA_EDGES[ei][1]];
          var rA = rotate3D(vA[0] * 0.48, vA[1] * 0.48, vA[2] * 0.48, wt * 0.8, wt * 1.1, 0.2);
          var rB = rotate3D(vB[0] * 0.48, vB[1] * 0.48, vB[2] * 0.48, wt * 0.8, wt * 1.1, 0.2);
          var pA = project3D(rA, cx, cy, fov, 4.2, 1.0);
          var pB = project3D(rB, cx, cy, fov, 4.2, 1.0);
          ctx.beginPath();
          ctx.moveTo(pA.x, pA.y);
          ctx.lineTo(pB.x, pB.y);
          ctx.stroke();
        }

        self.blitzState.animId = requestAnimationFrame(loopBlitz);
      }
      loopBlitz();
    },

    renderSpeedBlitzModal: function() {
      var existing = document.getElementById('matheduQuestBlitzModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduQuestBlitzModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(4,8,22,0.9);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:14px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      var bz = this.blitzState;
      var q = bz.pool[bz.qIdx % bz.pool.length];

      var optsHtml = q.options.map(function(opt, idx) {
        var num = idx + 1;
        return '<button type="button" onclick="window.MatheduQuest.submitBlitzOption(' + num + ')" ' +
          'style="padding:11px 14px;border-radius:12px;border:1.5px solid #cbd5e1;background:#ffffff;color:#0f172a;font-size:14px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:10px;text-align:left;transition:all .12s">' +
          '<span style="width:26px;height:26px;border-radius:999px;background:#fef3c7;color:#b45309;font-size:12px;font-weight:900;display:inline-flex;align-items:center;justify-content:center">' + num + '</span>' +
          '<span style="flex:1">' + opt + '</span>' +
        '</button>';
      }).join('');

      existing.innerHTML =
        '<div style="width:100%;max-width:660px;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 24px 52px rgba(0,0,0,0.65);border:2px solid #f59e0b">' +
          '<div style="background:linear-gradient(135deg,#0f172a 0%,#7c2d12 100%);color:#ffffff;padding:13px 18px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">' +
            '<div>' +
              '<div style="font-size:11px;color:#fbbf24;font-weight:800">🚀 60초 3D 스피드 디딤돌 블리츠 · 하이퍼워프 공식 타격</div>' +
              '<div style="font-size:16px;font-weight:900;margin-top:2px">⚡ [' + q.unit + '] 연속 격파 챌린지</div>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<button type="button" id="btnToggleMeditateBlitz" onclick="window.MatheduQuest.toggleMeditateMode()" style="padding:6px 12px;border-radius:999px;border:1px solid ' + (this.meditateMode ? '#5eead4' : 'rgba(255,255,255,0.28)') + ';background:' + (this.meditateMode ? 'linear-gradient(135deg,#0d9488 0%,#0284c7 100%)' : 'rgba(255,255,255,0.16)') + ';color:#ffffff;font-size:11.5px;font-weight:800;cursor:pointer">' +
                (this.meditateMode ? '🧘 사색 일시정지 ON (타이머 정지됨 · 클릭 시 재개)' : '🧘 사색 모드 (타이머 일시정지 & 생각 시간 갖기)') +
              '</button>' +
              '<button type="button" onclick="window.MatheduQuest.closeSpeedBlitzModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.16);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
            '</div>' +
          '</div>' +
          '<div style="position:relative;background:#040816;border-bottom:1.5px solid #1e293b">' +
            '<canvas id="questBlitz3DCanvas" width="640" height="115" style="width:100%;height:115px;display:block"></canvas>' +
            '<div style="position:absolute;top:10px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:center;pointer-events:none;font-size:12px;font-weight:900">' +
              '<span style="padding:4px 12px;border-radius:999px;background:rgba(239,68,68,0.88);color:#ffffff">⏱️ 남은 시간: <b id="questBlitzTimerText">' + bz.timeLeft + '초</b></span>' +
              '<span style="padding:4px 12px;border-radius:999px;background:rgba(15,23,42,0.85);color:#fbbf24;border:1px solid #fbbf24">🔥 ' + bz.combo + '콤보 · 🏆 격파 점수: ' + bz.score + '점</span>' +
            '</div>' +
          '</div>' +
          '<div style="padding:18px 20px">' +
            '<div style="font-size:15px;font-weight:800;color:#0f172a;line-height:1.7;margin-bottom:14px;padding:12px 14px;background:#fffbeb;border:1.5px solid #fde68a;border-radius:12px">' +
              q.stem +
            '</div>' +
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px">' +
              optsHtml +
            '</div>' +
            '<div id="questBlitzFeedback" style="margin-top:12px;font-size:12.5px;font-weight:700;color:#0369a1;min-height:20px">💡 ' + q.hint + '</div>' +
          '</div>' +
        '</div>';

      this.initBlitz3DCanvas();
      typesetMath(existing);
    },

    submitBlitzOption: function(chosenIdx) {
      var bz = this.blitzState;
      if (!bz.active) return;
      var q = bz.pool[bz.qIdx % bz.pool.length];
      if (chosenIdx === q.answer) {
        bz.combo++;
        bz.score += 10 + bz.combo * 2;
        this.state.combo = (this.state.combo || 0) + 1;
        this.state.ultimateGauge = Math.min(100, (this.state.ultimateGauge || 0) + 25);
        this.state.dailyQuests = ensureDailyQuests(this.state.dailyQuests);
        this.state.dailyQuests.stepsCleared = (this.state.dailyQuests.stepsCleared || 0) + 1;
        saveQuestState(this.state);
        this.playGameSfx('hit');
        bz.qIdx++;
        this.renderSpeedBlitzModal();
      } else {
        bz.combo = 0;
        this.playGameSfx('shield');
        var fb = document.getElementById('questBlitzFeedback');
        if (fb) {
          fb.style.color = '#b91c1c';
          fb.innerHTML = '🛡️ 방어막 발동! 힌트를 확인하세요: ' + q.hint + ' (정답: ' + q.answer + '번)';
          typesetMath(fb);
        }
      }
    },

    finishSpeedBlitzMode: function() {
      var bz = this.blitzState;
      bz.active = false;
      if (bz.timerId) {
        clearInterval(bz.timerId);
        bz.timerId = null;
      }
      if (bz.animId) {
        cancelAnimationFrame(bz.animId);
        bz.animId = null;
      }
      this.playGameSfx('victory');

      var bonusCsat = Math.min(8, Math.max(2, Math.round(bz.score / 25)));
      this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + bonusCsat);
      if (bz.score > (this.state.blitzBestScore || 0)) {
        this.state.blitzBestScore = bz.score;
      }
      saveQuestState(this.state);

      if (window.MatheduGame) {
        window.MatheduGame.addXP(Math.max(20, bz.score), '🚀 60초 3D 스피드 블리츠 완주! (+' + bonusCsat + '점)');
        if (typeof window.MatheduGame.fireConfetti === 'function') {
          window.MatheduGame.fireConfetti();
        }
      }

      var existing = document.getElementById('matheduQuestBlitzModal');
      if (existing) {
        existing.innerHTML =
          '<div style="width:100%;max-width:520px;background:#ffffff;border-radius:20px;padding:24px;text-align:center;box-shadow:0 24px 52px rgba(0,0,0,0.65);border:2px solid #fbbf24">' +
            '<div style="font-size:40px;margin-bottom:8px">🚀🏆</div>' +
            '<h3 style="margin:0 0 6px;font-size:20px;font-weight:900;color:#0f172a">60초 3D 스피드 디딤돌 블리츠 완료!</h3>' +
            '<p style="margin:0 0 14px;font-size:13.5px;color:#475569">총 <b>' + bz.qIdx + '문항</b> 돌파 · 블리츠 점수 <b>' + bz.score + '점</b> · 수능 만점 게이지 <b>+' + bonusCsat + '점</b> 상승!</p>' +
            '<div style="display:flex;gap:8px;justify-content:center">' +
              '<button type="button" onclick="window.MatheduQuest.startSpeedBlitzMode()" style="padding:10px 18px;border-radius:12px;border:none;background:linear-gradient(135deg,#ea580c 0%,#d97706 100%);color:#ffffff;font-size:13px;font-weight:900;cursor:pointer">🔥 한 번 더 스피드 도전</button>' +
              '<button type="button" onclick="window.MatheduQuest.closeSpeedBlitzModal()" style="padding:10px 18px;border-radius:12px;border:1px solid #cbd5e1;background:#f8fafc;color:#0f172a;font-size:13px;font-weight:800;cursor:pointer">월드맵으로 돌아가기</button>' +
            '</div>' +
          '</div>';
      }
      this.renderConsoleHub();
    },

    closeSpeedBlitzModal: function() {
      this.blitzState.active = false;
      if (this.blitzState.timerId) {
        clearInterval(this.blitzState.timerId);
        this.blitzState.timerId = null;
      }
      if (this.blitzState.animId) {
        cancelAnimationFrame(this.blitzState.animId);
        this.blitzState.animId = null;
      }
      var m = document.getElementById('matheduQuestBlitzModal');
      if (m) m.remove();
      this.renderConsoleHub();
    },

    renderConsoleHub: function() {
      var container = document.getElementById('matheduQuestConsoleRoot');
      if (!container) return;
      injectDesignerStylesheet();

      var st = this.state;
      st.dailyQuests = ensureDailyQuests(st.dailyQuests);
      var dq = st.dailyQuests;
      var activeW = this.getWorldById(st.activeWorldId);
      var pctScore = Math.min(100, Math.max(0, st.csatScore));
      var themeCfg = this.getThemeConfig(st.themeSkin);

      var worldTabsHtml = WORLDS.map(function(w) {
        var isAct = (w.id === activeW.id);
        var hasEmblem = st.emblems.indexOf(w.emblemId) !== -1;
        return '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.selectWorld(\'' + w.id + '\')" ' +
          'style="padding:8px 13px;border-radius:12px;border:1.5px solid ' + (isAct ? themeCfg.accent : 'rgba(255,255,255,0.16)') + ';' +
          'background:' + (isAct ? 'linear-gradient(135deg,#0284c7 0%,#2563eb 100%)' : 'rgba(255,255,255,0.06)') + ';' +
          'color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;display:inline-flex;align-items:center;gap:6px;box-shadow:' + (isAct ? '0 4px 14px rgba(56,189,248,0.35)' : 'none') + '">' +
          '<span>' + w.icon + ' World ' + w.num + '</span>' +
          (hasEmblem ? '<span title="대륙 정복 완료">✅</span>' : '') +
        '</button>';
      }).join('');

      var stagesHtml = activeW.stages.map(function(stg) {
        var isCleared = st.clearedStages.indexOf(stg.id) !== -1;
        return '<div style="padding:14px 18px;border-radius:14px;background:' + (isCleared ? '#f0fdf4' : '#ffffff') + ';border:1.5px solid ' + (isCleared ? '#86efac' : '#cbd5e1') + ';display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;box-shadow:0 2px 10px rgba(15,23,42,0.04)">' +
          '<div style="flex:1;min-width:210px">' +
            '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:5px">' +
              '<span style="padding:2px 9px;border-radius:999px;background:#e0f2fe;color:#0369a1;font-size:10.5px;font-weight:800">' + stg.gradeBadge + '</span>' +
              '<span style="padding:2px 9px;border-radius:999px;background:#fef3c7;color:#b45309;font-size:10.5px;font-weight:800">수능 +' + stg.scoreReward + '점 · +' + stg.xpReward + ' XP</span>' +
              (isCleared ? '<span style="padding:2px 9px;border-radius:999px;background:#dcfce7;color:#15803d;font-size:10.5px;font-weight:800">✅ 격파 완료</span>' : '') +
            '</div>' +
            '<div style="font-size:14.5px;font-weight:800;color:#0f172a;line-height:1.45">' + stg.bossName + '</div>' +
          '</div>' +
          '<div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap">' +
            '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.startStageById(\'' + activeW.id + '\',\'' + stg.id + '\')" ' +
              'style="padding:9px 15px;border-radius:11px;border:none;background:linear-gradient(135deg,#006398 0%,#2563eb 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 3px 10px rgba(37,99,235,0.25)">' +
              '⚔️ 3D 보스 배틀 시작' +
            '</button>' +
            '<a href="' + stg.url + '" class="quest-micro-btn" style="padding:8px 12px;border-radius:11px;border:1px solid #cbd5e1;background:#f8fafc;color:#334155;font-size:11.5px;font-weight:700;text-decoration:none">' +
              '🔎 풀스크린 퀴즈' +
            '</a>' +
          '</div>' +
        '</div>';
      }).join('');

      var minLinksHtml = (activeW.min7014Links || []).map(function(ml) {
        return '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.summonMin7014Grimoire(\'' + ml.url + '\')" ' +
          'style="padding:6px 12px;border-radius:999px;border:1px solid #bae6fd;background:#f0f9ff;color:#0369a1;font-size:11.5px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:5px">' +
          '<span>🔮 ' + ml.title + '</span>' +
          '<span style="font-size:10px;background:#0284c7;color:#fff;padding:1px 6px;border-radius:999px">+보호막·필살기 충전</span>' +
        '</button>';
      }).join('');

      var emblemsBar = WORLDS.map(function(w) {
        var unlocked = st.emblems.indexOf(w.emblemId) !== -1;
        return '<span style="padding:3px 9px;border-radius:999px;font-size:11px;font-weight:700;' +
          (unlocked ? 'background:#fef3c7;color:#92400e;border:1px solid #f59e0b' : 'background:rgba(255,255,255,0.08);color:#94a3b8;border:1px dashed rgba(255,255,255,0.2)') + '">' +
          w.emblemName + (unlocked ? ' ✨' : ' (미획득)') +
        '</span>';
      }).join('');

      var formulaBanner = this.getWorldMonumentFormulaDesc(activeW.id);
      var feverThresh = this.getFeverThreshold();
      var feverMult = this.getFeverMultiplier();
      var isFever = (st.combo || 0) >= feverThresh;
      var soundOn = (st.soundEnabled !== false);
      var wrongCount = (window.MatheduGame && typeof window.MatheduGame.getWrongAnswers === 'function')
        ? window.MatheduGame.getWrongAnswers().length
        : 0;

      var q1Done = dq.stepsCleared >= 3;
      var q2Done = dq.archiveSummoned >= 1;
      var q3Done = dq.grimoireOpened >= 1;
      var allDailyDone = q1Done && q2Done && q3Done;

      var selfRef = this;
      var eqRelics = st.equippedRelics || [];
      var equippedRelicsHtml = eqRelics.map(function(rid) {
        var r = selfRef.getRelicById(rid);
        if (!r) return '';
        return '<span title="' + r.desc + '" style="padding:3px 9px;border-radius:999px;background:rgba(251,191,36,0.16);border:1px solid #f59e0b;color:#fde047;font-size:11px;font-weight:800">' +
          r.icon + ' ' + r.name +
        '</span>';
      }).join('');

      var activeSynergies = this.getActiveSynergies();
      var synergiesHtml = activeSynergies.map(function(syn) {
        return '<span title="' + syn.desc + '" style="padding:3px 9px;border-radius:999px;background:rgba(16,185,129,0.22);border:1px solid #34d399;color:#6ee7b7;font-size:11px;font-weight:900">' +
          syn.name +
        '</span>';
      }).join('');

      var unlockedRelicsCount = (st.unlockedRelics || []).length;
      var unlockedStarsCount = (st.constellationStars || []).length;

      container.innerHTML =
        '<div class="quest-console-shell ' + themeCfg.cssClass + '" style="background:' + themeCfg.hubBg + ';border:1.5px solid ' + themeCfg.hubBorder + '">' +
          '<!-- 상단 타이틀 & 비주얼 테마 스위처 & 수능 100점 만점 게이지 HUD -->' +
          '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:14px">' +
            '<div style="flex:1;min-width:260px">' +
              '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:7px">' +
                '<span style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;background:rgba(56,189,248,0.16);border:1px solid ' + themeCfg.accent + ';color:' + themeCfg.accent + ';font-size:11px;font-weight:800">' +
                  '🌐 3D 수학 홀로그램 엔진 · mathteacher × gamemaker × designer × pr' +
                '</span>' +
                '<button type="button" id="btnCycleQuestThemeTop" class="quest-micro-btn" onclick="window.MatheduQuest.cycleQuestTheme()" ' +
                  'style="padding:4px 11px;border-radius:999px;border:1px solid ' + themeCfg.accent + ';background:rgba(255,255,255,0.1);color:#ffffff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px)">' +
                  '🎨 테마: ' + themeCfg.name + ' (🌌 코스믹 / 🧘 사색 서재 / 📜 유클리드)' +
                '</button>' +
                '<button type="button" id="btnOpenPrShareTop" class="quest-micro-btn" onclick="window.MatheduQuest.openPrShareModal()" ' +
                  'style="padding:4px 12px;border-radius:999px;border:1px solid #fbbf24;background:linear-gradient(135deg,#f59e0b 0%,#db2777 100%);color:#ffffff;font-size:11px;font-weight:900;cursor:pointer;backdrop-filter:blur(8px);box-shadow:0 2px 10px rgba(245,158,11,0.35)">' +
                  '📣 친구 도전장 & SNS 인증 공유' +
                '</button>' +
                '<button type="button" id="btnOpenRewardedAdTop" class="quest-micro-btn" onclick="if(window.MatheduAdEngine)window.MatheduAdEngine.openRewardedAdModal()" ' +
                  'style="padding:4px 12px;border-radius:999px;border:1px solid #34d399;background:linear-gradient(135deg,#059669 0%,#0284c7 100%);color:#ffffff;font-size:11px;font-weight:900;cursor:pointer;backdrop-filter:blur(8px);box-shadow:0 2px 10px rgba(16,185,129,0.35)">' +
                  '🎁 무료 광고 보너스 (+50 XP·필살기 완충)' +
                '</button>' +
              '</div>' +
              '<h2 style="margin:0;font-size:21px;font-weight:900;letter-spacing:-0.02em;color:#ffffff">👑 수능 수학 100점 만점 3D 원정대</h2>' +
              '<p style="margin:5px 0 0;font-size:12.5px;color:#cbd5e1;line-height:1.6">3D 입체 기하 모뉴먼트를 360° 회전하며 원리를 깊이 사색하고, 3중 수식 결계를 파쇄해 수능 100점 만점에 도달하세요!</p>' +
            '</div>' +
            '<div class="quest-hud-dock" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);min-width:230px;text-align:right">' +
              '<div style="font-size:11px;color:#93c5fd;font-weight:800">' + this.getGradeRankLabel(pctScore) + '</div>' +
              '<div style="font-size:23px;font-weight:900;color:#fbbf24;margin:3px 0">' + pctScore + ' <span style="font-size:13px;color:#e2e8f0">/ 100점 만점</span></div>' +
              '<div style="width:100%;height:8px;background:rgba(255,255,255,0.15);border-radius:999px;overflow:hidden">' +
                '<div style="width:' + pctScore + '%;height:100%;background:linear-gradient(90deg,#38bdf8,#fbbf24,#10b981);transition:width .35s ease"></div>' +
              '</div>' +
            '</div>' +
          '</div>' +

          '<!-- 📐 상단 HUD 액션 도크 그룹 1: 오늘의 수능 만점 일일 퀘스트 3종 & 🎁 황금 보물상자 -->' +
          '<div class="quest-hud-dock" style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px;background:' + themeCfg.dockBg + ';border:1px solid rgba(251,191,36,0.38)">' +
            '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:11.5px;font-weight:800">' +
              '<span style="color:#fbbf24">📜 오늘의 일일 퀘스트:</span>' +
              '<span style="padding:3px 10px;border-radius:999px;background:' + (q1Done ? 'rgba(16,185,129,0.25)' : 'rgba(255,255,255,0.08)') + ';border:1px solid ' + (q1Done ? '#34d399' : 'rgba(255,255,255,0.14)') + ';color:' + (q1Done ? '#34d399' : '#cbd5e1') + '">① 디딤돌 돌파 (' + Math.min(3, dq.stepsCleared) + '/3) ' + (q1Done ? '✅' : '') + '</span>' +
              '<span style="padding:3px 10px;border-radius:999px;background:' + (q2Done ? 'rgba(16,185,129,0.25)' : 'rgba(255,255,255,0.08)') + ';border:1px solid ' + (q2Done ? '#34d399' : 'rgba(255,255,255,0.14)') + ';color:' + (q2Done ? '#34d399' : '#cbd5e1') + '">② 기출·약점 보스 소환 (' + Math.min(1, dq.archiveSummoned) + '/1) ' + (q2Done ? '✅' : '') + '</span>' +
              '<span style="padding:3px 10px;border-radius:999px;background:' + (q3Done ? 'rgba(16,185,129,0.25)' : 'rgba(255,255,255,0.08)') + ';border:1px solid ' + (q3Done ? '#34d399' : 'rgba(255,255,255,0.14)') + ';color:' + (q3Done ? '#34d399' : '#cbd5e1') + '">③ min7014 비급서 탐구 (' + Math.min(1, dq.grimoireOpened) + '/1) ' + (q3Done ? '✅' : '') + '</span>' +
            '</div>' +
            (dq.chestClaimed
              ? '<span style="font-size:11.5px;font-weight:800;color:#fde047">🎁 오늘의 황금 보물상자 수령 완료!</span>'
              : '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.claimDailyTreasureChest()" ' +
                  (allDailyDone ? '' : 'disabled ') +
                  'style="padding:6px 13px;border-radius:999px;border:1px solid ' + (allDailyDone ? '#fde047' : 'rgba(255,255,255,0.2)') + ';background:' + (allDailyDone ? 'linear-gradient(135deg,#f59e0b 0%,#d97706 100%)' : 'rgba(255,255,255,0.08)') + ';color:' + (allDailyDone ? '#ffffff' : '#94a3b8') + ';font-size:11.5px;font-weight:900;cursor:' + (allDailyDone ? 'pointer' : 'not-allowed') + '">' +
                  '🎁 황금 보물상자 열기 (+수능 5점 · +100 XP)' +
                '</button>') +
          '</div>' +

          '<!-- 📐 상단 HUD 액션 도크 그룹 2: 수학자의 성물(Relics) & 4대 수학 성좌(Constellations) -->' +
          '<div class="quest-hud-dock" style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:14px;background:' + themeCfg.dockBg + ';border:1px solid ' + themeCfg.dockBorder + '">' +
            '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:11.5px;font-weight:800">' +
              '<span style="color:#c4b5fd">🃏 장착 성물 (' + eqRelics.length + '/3):</span>' +
              (equippedRelicsHtml || '<span style="color:#94a3b8">장착된 성물 없음</span>') +
              synergiesHtml +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap">' +
              '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.openRelicDraftModal(true)" ' +
                'style="padding:6px 13px;border-radius:999px;border:1px solid #f59e0b;background:linear-gradient(135deg,#b45309 0%,#d97706 100%);color:#ffffff;font-size:11.5px;font-weight:900;cursor:pointer">' +
                '🃏 수학 성물 3택1 드래프트 & 도감 (' + unlockedRelicsCount + '/' + MATH_RELICS.length + ')' +
              '</button>' +
              '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.openConstellationModal()" ' +
                'style="padding:6px 13px;border-radius:999px;border:1px solid #818cf8;background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);color:#ffffff;font-size:11.5px;font-weight:900;cursor:pointer">' +
                '🌌 4대 수학 성좌 각성 트리 (' + unlockedStarsCount + '/12 ★)' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<!-- 6대 대륙 월드맵 탭 -->' +
          '<div style="display:flex;align-items:center;gap:7px;overflow-x:auto;padding-bottom:8px;margin-bottom:10px">' +
            worldTabsHtml +
          '</div>' +

          '<!-- 🌐 실시간 3D 수학 기하 홀로그램 뷰포트 (360° 드래그 회전 & 줌 & X-Ray 투시 & 테마 스킨) -->' +
          '<div style="position:relative;border-radius:16px;overflow:hidden;border:1.5px solid ' + (isFever ? '#fbbf24' : themeCfg.accent) + ';margin-bottom:14px;background:' + themeCfg.canvasBgStops[2] + '">' +
            '<canvas id="matheduQuest3DCanvas" width="720" height="270" style="width:100%;height:250px;display:block;cursor:grab"></canvas>' +
            '<!-- 좌상단 3D 수식 구조물 배지 & FEVER RUSH 배지 -->' +
            '<div style="position:absolute;top:10px;left:12px;right:12px;display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;pointer-events:none">' +
              '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
                '<span style="padding:4px 11px;border-radius:999px;background:rgba(15,23,42,0.82);border:1px solid ' + themeCfg.accent + ';color:#e0f2fe;font-size:11.5px;font-weight:800;backdrop-filter:blur(8px)">' +
                  formulaBanner +
                '</span>' +
                (isFever ? '<span style="padding:4px 10px;border-radius:999px;background:linear-gradient(135deg,#f59e0b 0%,#ea580c 100%);border:1px solid #fde047;color:#ffffff;font-size:11px;font-weight:900;box-shadow:0 0 14px rgba(251,191,36,0.65)">🔥 FEVER RUSH (' + st.combo + '연속 콤보 가속 중! 보상 XP ' + feverMult.toFixed(1) + '배)</span>' : '') +
              '</div>' +
              '<span style="padding:3px 10px;border-radius:999px;background:rgba(15,23,42,0.78);color:#93c5fd;font-size:10.5px;font-weight:700;backdrop-filter:blur(8px)">' +
                '🖱️ 드래그: 360° 회전 · 휠: 줌' +
              '</span>' +
            '</div>' +
            '<!-- 하단 3D 인터랙티브 컨트롤 바 -->' +
            '<div style="position:absolute;bottom:10px;left:12px;right:12px;display:flex;align-items:center;justify-content:space-between;gap:6px;flex-wrap:wrap">' +
              '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
                '<button type="button" id="btnToggle3DXray" class="quest-micro-btn" onclick="window.MatheduQuest.toggleXrayMode()" ' +
                  'style="padding:5px 11px;border-radius:999px;border:1px solid #34d399;background:rgba(16,185,129,0.28);color:#ffffff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px)">' +
                  '📐 수학 보조선·정사영 투시 ON' +
                '</button>' +
                '<button type="button" id="btnToggle3DGalaxy" class="quest-micro-btn" onclick="window.MatheduQuest.toggleGalaxyMode()" ' +
                  'style="padding:5px 11px;border-radius:999px;border:1px solid rgba(56,189,248,0.5);background:rgba(14,165,233,0.25);color:#ffffff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px)">' +
                  '🌌 6대 대륙 3D 행성계 전체 성좌 보기' +
                '</button>' +
                '<button type="button" id="btnCycleQuestThemeViewport" class="quest-micro-btn" onclick="window.MatheduQuest.cycleQuestTheme()" ' +
                  'style="padding:5px 11px;border-radius:999px;border:1px solid ' + themeCfg.accent + ';background:rgba(139,92,246,0.28);color:#ffffff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px)">' +
                  '🎨 테마: ' + themeCfg.shortLabel +
                '</button>' +
                '<button type="button" id="btnToggle3DSound" class="quest-micro-btn" onclick="window.MatheduQuest.toggleSound()" ' +
                  'style="padding:5px 11px;border-radius:999px;border:1px solid ' + (soundOn ? '#fbbf24' : 'rgba(255,255,255,0.2)') + ';background:' + (soundOn ? 'rgba(251,191,36,0.25)' : 'rgba(255,255,255,0.1)') + ';color:#ffffff;font-size:11px;font-weight:800;cursor:pointer;backdrop-filter:blur(8px)">' +
                  (soundOn ? '🔊 효과음 ON' : '🔇 효과음 OFF') +
                '</button>' +
              '</div>' +
              '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.resetCamera3D()" ' +
                'style="padding:5px 10px;border-radius:999px;border:1px solid rgba(255,255,255,0.25);background:rgba(15,23,42,0.78);color:#cbd5e1;font-size:11px;font-weight:700;cursor:pointer;backdrop-filter:blur(8px)">' +
                '🔄 시점 초기화' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<!-- 획득한 마스터 엠블럼 컬렉션 -->' +
          '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:14px;padding:9px 14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:13px">' +
            '<span style="font-size:11.5px;font-weight:800;color:#e2e8f0;margin-right:4px">🏆 정복 엠블럼:</span>' +
            emblemsBar +
          '</div>' +

          '<!-- 선택된 대륙 상세 카드 -->' +
          '<div style="background:#f8fafc;color:#0f172a;border-radius:18px;padding:18px;box-shadow:0 8px 24px rgba(0,0,0,0.18)">' +
            '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:12px">' +
              '<div>' +
                '<div style="font-size:16.5px;font-weight:900;color:#0f172a">' + activeW.icon + ' ' + activeW.name + '</div>' +
                '<div style="font-size:12px;color:#475569;font-weight:600;margin-top:3px">' + activeW.sub + '</div>' +
              '</div>' +
              '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
                '<button type="button" id="btnStartSpeedBlitz" class="quest-micro-btn" onclick="window.MatheduQuest.startSpeedBlitzMode()" ' +
                  'style="padding:9px 14px;border-radius:12px;border:1.5px solid #ea580c;background:linear-gradient(135deg,#ea580c 0%,#d97706 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(234,88,12,0.28)">' +
                  '🚀 60초 3D 스피드 공식 블리츠' + (st.blitzBestScore ? ' (최고 ' + st.blitzBestScore + '점)' : '') +
                '</button>' +
                '<button type="button" id="btnSummonArchiveBoss" class="quest-micro-btn" onclick="window.MatheduQuest.summonRandomArchiveProblem(\'' + activeW.id + '\')" ' +
                  'style="padding:9px 14px;border-radius:12px;border:1.5px solid #7c3aed;background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(124,58,237,0.25)">' +
                  '🎲 이 대륙의 3D 기출 보스 무작위 소환 (16,548문항 DB)' +
                '</button>' +
                '<button type="button" id="btnSummonRevengeBoss" class="quest-micro-btn" onclick="window.MatheduQuest.summonWeaknessRevengeBoss(\'' + activeW.id + '\')" ' +
                  'style="padding:9px 14px;border-radius:12px;border:1.5px solid #e11d48;background:linear-gradient(135deg,#e11d48 0%,#be123c 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(225,29,72,0.25)">' +
                  '⚡ 약점 3D 리벤지 레이드' + (wrongCount > 0 ? ' (' + wrongCount + '문항 대기)' : '') +
                '</button>' +
              '</div>' +
            '</div>' +

            '<!-- mathteacher 에이전트 수학 조언 브리핑 -->' +
            '<div style="padding:11px 15px;border-radius:12px;background:#eff6ff;border-left:4px solid #0284c7;font-size:12.5px;color:#1e3a8a;margin-bottom:14px;line-height:1.65">' +
              '<b>👩‍🏫 [mathteacher 수석 교사 브리핑]</b> ' + activeW.teacherAdvice +
            '</div>' +

            '<!-- 스테이지 / 보스 목록 -->' +
            '<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:14px">' +
              stagesHtml +
            '</div>' +

            '<!-- 민은기 선생님(min7014.github.io) 시각 증명 비급서 소환 바 -->' +
            '<div style="padding-top:11px;border-top:1px dashed #cbd5e1;display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
              '<span style="font-size:11.5px;font-weight:800;color:#0369a1">📐 민은기 선생님(min7014.github.io) 시각 증명 비급서:</span>' +
              minLinksHtml +
            '</div>' +
          '</div>' +
        '</div>';

      this.initMain3DCanvas();
      typesetMath(container);
    },

    renderBattleModal: function() {
      var stg = this.activeStage;
      if (!stg) return;
      injectDesignerStylesheet();

      var existing = document.getElementById('matheduQuestBattleModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduQuestBattleModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(6,11,25,0.88);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;padding:14px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      var totalSteps = stg.steps.length;
      var curStep = stg.steps[this.activeStepIdx] || stg.steps[0];
      var bossHpPct = Math.max(0, Math.round(((totalSteps - this.activeStepIdx) / totalSteps) * 100));
      var feverThresh = this.getFeverThreshold();
      var feverMult = this.getFeverMultiplier();
      var isFever = (this.state.combo || 0) >= feverThresh;
      var ultPct = Math.min(100, Math.max(0, this.state.ultimateGauge || 0));
      var ultReady = ultPct >= 100;
      var themeCfg = this.getThemeConfig(this.state.themeSkin);

      // 🧭 데카르트의 좌표평면 조준경: 각 단계 시작 시 함정 오답 1개 자동 투시 소거
      var descartesElimIdx = -1;
      if (this.hasRelic('relic_descartes')) {
        var ansIdx = parseInt(curStep.answer, 10);
        var candWrong = [];
        for (var wi = 1; wi <= (curStep.options || []).length; wi++) {
          if (wi !== ansIdx) candWrong.push(wi);
        }
        if (candWrong.length > 0) {
          descartesElimIdx = candWrong[(this.activeStepIdx * 3) % candWrong.length];
        }
      }

      var symHtml = (stg.symbols || []).map(function(s) {
        return '<div style="padding:7px 11px;background:#ffffff;border:1px solid #bae6fd;border-radius:9px;font-size:12.5px;color:#0f172a;line-height:1.6">' +
          '<b>' + s.sym + '</b> — ' + s.desc +
        '</div>';
      }).join('');

      var optsHtml = (curStep.options || []).map(function(opt, i) {
        var optNum = i + 1;
        var isDescartesElim = (optNum === descartesElimIdx);
        return '<button type="button" class="quest-battle-opt-btn quest-opt-btn" onclick="window.MatheduQuest.submitBattleOption(' + optNum + ')" ' +
          (isDescartesElim ? 'disabled ' : '') +
          'style="background:' + (isDescartesElim ? '#f1f5f9' : '#ffffff') + ';cursor:' + (isDescartesElim ? 'not-allowed' : 'pointer') + ';opacity:' + (isDescartesElim ? '0.45' : '1') + ';text-decoration:' + (isDescartesElim ? 'line-through' : 'none') + '">' +
          '<span style="width:28px;height:28px;border-radius:999px;background:#f1f5f9;color:#0f172a;font-weight:800;font-size:12.5px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0">' + optNum + '</span>' +
          '<span style="flex:1;line-height:1.72">' + opt + (isDescartesElim ? ' <b style="color:#dc2626;font-size:11px">(🧭 데카르트 성물 함정 소거)</b>' : '') + '</span>' +
        '</button>';
      }).join('');

      var selfRef = this;
      var battleRelicsBar = (this.state.equippedRelics || []).map(function(rid) {
        var r = selfRef.getRelicById(rid);
        return r ? ('<span title="' + (r.effectDesc || '') + '" style="padding:2px 8px;border-radius:999px;background:rgba(251,191,36,0.2);border:1px solid #fbbf24;color:#fde047;font-size:10.5px;font-weight:800">' + r.icon + ' ' + r.name + '</span>') : '';
      }).join(' ');

      var curInsightPct = Math.min(100, Math.max(0, Math.round(this.insightGauge || 0)));
      var pSteps = this.polyaSteps || { s1: false, s2: false, s3: false };

      existing.innerHTML =
        '<div id="questBattleModalCard" class="quest-battle-modal-card ' + themeCfg.cssClass + (this.meditateMode ? ' quest-meditate-active' : '') + '" style="width:100%;max-width:740px;background:#ffffff;border-radius:22px;overflow:hidden;box-shadow:0 24px 52px rgba(0,0,0,0.58);border:2px solid ' + (isFever ? '#fbbf24' : themeCfg.accent) + ';max-height:94vh;display:flex;flex-direction:column">' +
          '<!-- 전투 상단 헤더 -->' +
          '<div style="background:' + themeCfg.battleHeaderGrad + ';color:#ffffff;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">' +
            '<div>' +
              '<div style="font-size:11px;color:' + themeCfg.accent + ';font-weight:800">' + stg.gradeBadge + '</div>' +
              '<div style="font-size:16.5px;font-weight:900;margin-top:2px">' + stg.bossName + '</div>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
              '<button type="button" id="btnToggleMeditateBattle" class="quest-micro-btn" onclick="window.MatheduQuest.toggleMeditateMode()" style="padding:6px 12px;border-radius:999px;border:1px solid ' + (this.meditateMode ? '#fbbf24' : 'rgba(255,255,255,0.28)') + ';background:' + (this.meditateMode ? 'linear-gradient(135deg,#7c3aed 0%,#0d9488 100%)' : 'rgba(255,255,255,0.16)') + ';color:#ffffff;font-size:11.5px;font-weight:800;cursor:pointer">' +
                (this.meditateMode ? '🧘 사색 모드 ON (결계 감속 · 통찰 2배 충전 중)' : '🧘 사색 모드 (생각 시간 갖기)') +
              '</button>' +
              '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.cycleQuestTheme()" style="padding:6px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.28);background:rgba(255,255,255,0.14);color:#ffffff;font-size:11px;font-weight:800;cursor:pointer">' +
                '🎨 ' + themeCfg.shortLabel +
              '</button>' +
              '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.openPrShareModal(true)" style="padding:6px 11px;border-radius:999px;border:1px solid #fbbf24;background:linear-gradient(135deg,#f59e0b 0%,#db2777 100%);color:#ffffff;font-size:11px;font-weight:900;cursor:pointer">' +
                '📣 친구 도전장 & SNS 인증 공유' +
              '</button>' +
              '<a href="' + stg.url + '" style="padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.16);color:#ffffff;font-size:11.5px;font-weight:700;text-decoration:none">🔎 풀스크린 열기</a>' +
              '<button type="button" onclick="window.MatheduQuest.closeBattleModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.16);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
            '</div>' +
          '</div>' +

          '<!-- ⚔️ 실시간 3D 보스 코어 & 3중 짐벌 수식 결계 링 뷰포트 -->' +
          '<div style="position:relative;background:#020617;border-bottom:1.5px solid #1e293b">' +
            '<canvas id="questBattle3DCanvas" width="680" height="150" style="width:100%;height:145px;display:block"></canvas>' +
            '<div style="position:absolute;top:8px;left:14px;right:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;pointer-events:none;font-size:11.5px;font-weight:800">' +
              '<span style="padding:3px 10px;border-radius:999px;background:rgba(15,23,42,0.82);color:#f87171;border:1px solid rgba(248,113,113,0.4);backdrop-filter:blur(8px)">👾 3D 보스 결계 장갑: ' + bossHpPct + '% (남은 결계 ' + (totalSteps - this.activeStepIdx) + '겹)</span>' +
              '<span style="padding:3px 10px;border-radius:999px;background:' + (isFever ? 'linear-gradient(135deg,#f59e0b 0%,#ea580c 100%)' : 'rgba(15,23,42,0.82)') + ';color:' + (isFever ? '#ffffff' : '#38bdf8') + ';border:1px solid ' + (isFever ? '#fde047' : 'rgba(56,189,248,0.4)') + ';backdrop-filter:blur(8px)">🛡️ 디딤돌 보호막: <b id="questBattleShieldText">' + this.state.shieldHp + '%</b> · 🔥 ' + this.state.combo + '콤보' + (isFever ? ' (FEVER RUSH · XP ' + feverMult.toFixed(1) + '배!)' : '') + '</span>' +
            '</div>' +
            (battleRelicsBar ? '<div style="position:absolute;bottom:6px;left:14px;display:flex;gap:4px;flex-wrap:wrap;pointer-events:none">' + battleRelicsBar + '</div>' : '') +
          '</div>' +

          '<!-- 전투 본문 스크롤 영역 -->' +
          '<div style="padding:18px 22px;overflow-y:auto;flex:1">' +
            '<!-- 🧠 아르키메데스의 사색 통찰력 축적 게이지 (Insight Resonance Gauge) -->' +
            '<div style="margin-bottom:12px;padding:12px 16px;border-radius:14px;background:#f8fafc;border:1.5px solid #cbd5e1">' +
              '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:7px">' +
                '<span style="font-size:12px;font-weight:900;color:#0f172a">🧠 아르키메데스의 사색 통찰력 게이지: <b id="questInsightGaugeText" style="color:#0284c7">' + curInsightPct + '%</b></span>' +
                '<span id="questInsightStatusBadge" style="padding:2px 9px;border-radius:999px;font-size:11px;font-weight:800;background:#f1f5f9;color:#475569">⏳ 문제를 읽고 조건을 분석하며 통찰력을 모으는 중...</span>' +
              '</div>' +
              '<div style="width:100%;height:8px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin-bottom:9px">' +
                '<div id="questInsightGaugeFill" style="width:' + curInsightPct + '%;height:100%;background:linear-gradient(90deg,#64748b,#38bdf8);transition:width .15s linear"></div>' +
              '</div>' +
              '<!-- 🎯 폴리아(G. Polya)의 3단계 생각 징검다리 & ✏️ 데카르트 연습장 버튼 바 -->' +
              '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap">' +
                '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
                  '<span style="font-size:11px;font-weight:800;color:#475569">🎯 폴리아 생각 징검다리:</span>' +
                  '<button type="button" id="btnPolyaStep1" class="quest-polya-pill" onclick="window.MatheduQuest.togglePolyaStep(1)" style="border:1px solid ' + (pSteps.s1 ? '#22c55e' : '#94a3b8') + ';background:' + (pSteps.s1 ? '#dcfce7' : '#ffffff') + ';color:' + (pSteps.s1 ? '#15803d' : '#334155') + '">🎯 ① 구하는 것 확인 (+30%)</button>' +
                  '<button type="button" id="btnPolyaStep2" class="quest-polya-pill" onclick="window.MatheduQuest.togglePolyaStep(2)" style="border:1px solid ' + (pSteps.s2 ? '#22c55e' : '#94a3b8') + ';background:' + (pSteps.s2 ? '#dcfce7' : '#ffffff') + ';color:' + (pSteps.s2 ? '#15803d' : '#334155') + '">🔑 ② 주어진 조건 분해 (+35%)</button>' +
                  '<button type="button" id="btnPolyaStep3" class="quest-polya-pill" onclick="window.MatheduQuest.togglePolyaStep(3)" style="border:1px solid ' + (pSteps.s3 ? '#22c55e' : '#94a3b8') + ';background:' + (pSteps.s3 ? '#dcfce7' : '#ffffff') + ';color:' + (pSteps.s3 ? '#15803d' : '#334155') + '">🌉 ③ 연결 공식·보조선 구상 (+35%)</button>' +
                '</div>' +
                '<button type="button" id="btnToggleScratchpad" class="quest-micro-btn" onclick="window.MatheduQuest.toggleScratchpad()" style="padding:5px 12px;border-radius:999px;border:1.5px solid #0284c7;background:' + (this.scratchpadOpen ? '#0284c7' : '#f0f9ff') + ';color:' + (this.scratchpadOpen ? '#ffffff' : '#0369a1') + ';font-size:11px;font-weight:900;cursor:pointer">' +
                  (this.scratchpadOpen ? '✏️ 생각 연습장 닫기' : '✏️ 생각 연습장 (Scratchpad)') +
                '</button>' +
              '</div>' +
              '<div id="questPolyaCoachingBox" style="display:none;margin-top:9px;padding:9px 13px;border-radius:10px;background:#f0fdf4;border:1px solid #86efac;color:#14532d;font-size:12.5px;line-height:1.65"></div>' +
            '</div>' +

            '<!-- ✏️ 인게임 데카르트의 디지털 수학 연습장 (Interactive Scratchpad Canvas) -->' +
            '<div id="questScratchpadWrap" style="display:' + (this.scratchpadOpen ? 'block' : 'none') + ';margin-bottom:14px;padding:12px 14px;border-radius:14px;background:#0f172a;border:1.5px solid #38bdf8;color:#ffffff;backdrop-filter:blur(16px)">' +
              '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:8px">' +
                '<span id="questScratchpadStatusBadge" style="font-size:11.5px;font-weight:800;color:' + (this.scratchpadUsed ? '#34d399' : '#bae6fd') + '">' +
                  (this.scratchpadUsed
                    ? '✍️ 데카르트 연습장 활성화됨! (통찰 +40% 충전 완료 · 정답 시 +15 XP 보너스)'
                    : '✏️ 마우스나 터치펜으로 수식·그래프·보조선을 자유롭게 그려보세요! (+통찰 40% & +15 XP)') +
                '</span>' +
                '<div style="display:flex;align-items:center;gap:5px">' +
                  '<button type="button" onclick="window.MatheduQuest.setScratchpadColor(\'#f8fafc\')" style="width:20px;height:20px;border-radius:999px;border:2px solid #cbd5e1;background:#f8fafc;cursor:pointer" title="화이트 펜"></button>' +
                  '<button type="button" onclick="window.MatheduQuest.setScratchpadColor(\'#38bdf8\')" style="width:20px;height:20px;border-radius:999px;border:2px solid #cbd5e1;background:#38bdf8;cursor:pointer" title="시안 펜"></button>' +
                  '<button type="button" onclick="window.MatheduQuest.setScratchpadColor(\'#fbbf24\')" style="width:20px;height:20px;border-radius:999px;border:2px solid #cbd5e1;background:#fbbf24;cursor:pointer" title="골드 펜"></button>' +
                  '<button type="button" onclick="window.MatheduQuest.setScratchpadColor(\'#fb7185\')" style="width:20px;height:20px;border-radius:999px;border:2px solid #cbd5e1;background:#fb7185;cursor:pointer" title="코랄 펜"></button>' +
                  '<button type="button" onclick="window.MatheduQuest.clearScratchpad()" style="padding:3px 9px;border-radius:999px;border:1px solid #64748b;background:#1e293b;color:#e2e8f0;font-size:11px;font-weight:800;cursor:pointer">🗑️ 지우기</button>' +
                '</div>' +
              '</div>' +
              '<canvas id="questScratchpadCanvas" width="640" height="175" style="width:100%;height:175px;display:block;border-radius:9px;border:1px solid #334155;cursor:crosshair;touch-action:none"></canvas>' +
            '</div>' +

            '<!-- 제0단계 수학 기호 번역기 마법서 -->' +
            '<details id="questSymbolTranslatorDetails" style="margin-bottom:13px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:13px;padding:10px 15px" open>' +
              '<summary style="font-size:12px;font-weight:800;color:#0369a1;cursor:pointer">🔰 [제0단계 기호 번역기 마법서] 낯선 수학 기호 한눈에 번역하기</summary>' +
              '<div style="display:flex;flex-direction:column;gap:6px;margin-top:8px">' + symHtml + '</div>' +
            '</details>' +

            '<!-- 현재 단계 지식 가이드 -->' +
            '<div style="margin-bottom:13px;padding:12px 16px;background:#f8fafc;border-left:4px solid #0284c7;border-radius:11px">' +
              '<div style="font-size:13px;font-weight:900;color:#006398;margin-bottom:4px">' + curStep.label + '</div>' +
              '<div style="font-size:12.5px;color:#334155;line-height:1.68">💡 <b>[mathteacher 디딤돌 힌트]</b> ' + curStep.know + '</div>' +
            '</div>' +

            '<!-- 🌟 기하 통찰 필살기 발동 바 (오답 2개 제거 & 수식 단서) -->' +
            '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:12px;padding:9px 14px;border-radius:13px;background:#fffbeb;border:1px solid #fde68a">' +
              '<div style="font-size:12px;font-weight:800;color:#92400e">⚡ 기하 통찰 필살기 게이지: <b>' + Math.round(ultPct) + '%</b></div>' +
              '<button type="button" id="btnCastGeometricUltimate" class="quest-micro-btn" onclick="window.MatheduQuest.castGeometricUltimate()" ' +
                (ultReady ? '' : 'disabled ') +
                'style="padding:6px 13px;border-radius:999px;border:none;background:' + (ultReady ? 'linear-gradient(135deg,#f59e0b 0%,#ea580c 100%)' : '#cbd5e1') + ';color:#ffffff;font-size:11.5px;font-weight:900;cursor:' + (ultReady ? 'pointer' : 'not-allowed') + ';box-shadow:' + (ultReady ? '0 2px 10px rgba(245,158,11,0.4)' : 'none') + '">' +
                (ultReady ? '🌟 기하 통찰 필살기 발동 (오답 2개 즉시 소거!)' : '⚡ 필살기 충전 중 (' + Math.round(ultPct) + '% / 단계 통과 시 +35%)') +
              '</button>' +
            '</div>' +
            '<div id="questUltimateInsightBox" style="display:none;margin-bottom:12px;padding:11px 15px;border-radius:11px;background:#fef3c7;border:1.5px solid #f59e0b;font-size:12.5px;color:#78350f;line-height:1.65"></div>' +

            '<!-- 발문 (.quest-battle-stem 황금비 타이포그래피 & 사색 모드 오로라 광채) -->' +
            '<div id="questBattleStemBox" class="quest-battle-stem' + (this.meditateMode ? ' quest-meditate-active' : '') + '">' +
              curStep.stem +
            '</div>' +

            '<!-- 5지선다 버튼 (.quest-opt-btn) -->' +
            '<div id="questBattleOptsWrap" style="display:flex;flex-direction:column;gap:8px">' +
              optsHtml +
            '</div>' +

            '<!-- 정답/오답 피드백 및 다음 단계 버튼 -->' +
            '<div id="questBattleFeedbackBox" style="display:none;margin-top:14px;padding:15px;border-radius:13px"></div>' +
          '</div>' +
        '</div>';

      this.initBattle3DCanvas();
      this.updateInsightGaugeDOM();
      if (this.scratchpadOpen) {
        this.initScratchpadCanvas();
      }
      typesetMath(existing);
    },

    submitBattleOption: function(chosenIdx) {
      var stg = this.activeStage;
      if (!stg) return;
      var curStep = stg.steps[this.activeStepIdx];
      if (!curStep) return;

      this.stepAttempts = (this.stepAttempts || 0) + 1;
      var elapsedSec = (Date.now() - (this.stepStartTime || Date.now())) / 1000;
      var critLimit = this.hasConstellationStar('c2_s2') ? 20 : 15;

      var isCorrect = (chosenIdx === parseInt(curStep.answer, 10));
      var fb = document.getElementById('questBattleFeedbackBox');
      if (!fb) return;

      fb.style.display = 'block';
      if (isCorrect) {
        var curInsight = Math.round(this.insightGauge || 0);
        var isDeepEureka = (this.stepAttempts === 1 && (curInsight >= 90 || elapsedSec >= 15));
        var isThoughtfulSolve = (this.stepAttempts === 1 && !isDeepEureka && curInsight >= 50);
        var isCritDerivation = (this.stepAttempts === 1 && elapsedSec <= critLimit);
        var hasScratchpadBonus = !!this.scratchpadUsed;

        var shieldGain = 15 + (this.hasRelic('relic_cauchy') ? 10 : 0);
        var ultGain = 35 + (this.hasRelic('relic_fermat') ? 10 : 0) + (this.hasConstellationStar('c4_s1') ? 10 : 0) + (isCritDerivation ? 15 : 0) + (isDeepEureka ? 35 : 0);

        if (isDeepEureka) {
          var eurekaCsatBonus = 1 + (this.hasRelic('relic_archimedes') ? 2 : 0);
          this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + eurekaCsatBonus);
          this.battle3D.supernovaTimer = 30;
          this.playGameSfx('eureka');
          this.spawnFloatingText('🧠 DEEP EUREKA!! (+40 XP · 수능 +' + eurekaCsatBonus + '점)', '#fde047', -22);
        } else if (isThoughtfulSolve) {
          this.spawnFloatingText('💡 THOUGHTFUL SOLVE! (깊은 논리 도출 +20 XP)', '#38bdf8', -20);
        }

        if (hasScratchpadBonus) {
          this.spawnFloatingText('✍️ DESCARTES SCRATCHPAD BONUS! (+15 XP)', '#a78bfa', 16);
        }

        this.state.combo = (this.state.combo || 0) + 1;
        this.state.shieldHp = Math.min(100, (this.state.shieldHp || 80) + shieldGain);
        this.state.ultimateGauge = Math.min(100, (this.state.ultimateGauge || 0) + ultGain);
        this.state.dailyQuests = ensureDailyQuests(this.state.dailyQuests);
        this.state.dailyQuests.stepsCleared = (this.state.dailyQuests.stepsCleared || 0) + 1;
        saveQuestState(this.state);

        // 3D 결계 파쇄 파티클 폭발 & 레이저 빔 발동!
        var ringColors = ['#38bdf8', '#fbbf24', '#f43f5e'];
        this.spawnRingShatterParticles(ringColors[this.activeStepIdx % 3]);

        var isLastStep = (this.activeStepIdx >= stg.steps.length - 1);
        var partBreakLabel = '';
        if (isLastStep) {
          partBreakLabel = '✨ ALL-OUT GEOMETRIC FINISH! — Q.E.D. ✨';
          this.battle3D.allOutSlashTimer = 42;
          this.playGameSfx('victory');
          this.spawnFloatingText('✨ ALL-OUT GEOMETRIC FINISH! — Q.E.D. ✨', '#fde047', 0);
        } else if (this.activeStepIdx === 0) {
          partBreakLabel = '💥 PART BREAK [1/' + stg.steps.length + ']: 외곽 기호 결계 파쇄!';
          if (!isDeepEureka) this.playGameSfx('hit');
          this.spawnFloatingText('💥 PART BREAK! [외곽 결계 파쇄]', '#38bdf8', 0);
        } else {
          partBreakLabel = '💥 ARMOR BREAK [2/' + stg.steps.length + ']: 중간 유도 장갑 붕괴!';
          if (!isDeepEureka) this.playGameSfx('hit');
          this.spawnFloatingText('💥 ARMOR BREAK! [중간 장갑 붕괴]', '#fbbf24', 0);
        }

        if (isCritDerivation && !isDeepEureka) {
          this.spawnFloatingText('⚡ CRITICAL DERIVATION! (' + elapsedSec.toFixed(1) + '초 돌파 · XP 1.5x)', '#34d399', -14);
        }

        var feverThresh = this.getFeverThreshold();
        var feverMult = this.getFeverMultiplier();
        var isFever = this.state.combo >= feverThresh;
        var baseXp = 15 + (this.hasConstellationStar('c1_s1') ? 5 : 0);
        var stepXp = Math.round(baseXp * (isFever ? feverMult : 1.0) * (isCritDerivation ? 1.5 : 1.0));
        if (isDeepEureka) stepXp += 40;
        else if (isThoughtfulSolve) stepXp += 20;
        if (hasScratchpadBonus) stepXp += 15;

        if (window.MatheduGame) {
          window.MatheduGame.recordActivity();
          window.MatheduGame.addXP(
            stepXp,
            curStep.label + ' ' + partBreakLabel +
            (isDeepEureka ? ' (🧠 DEEP EUREKA!! +40 XP)' : (isThoughtfulSolve ? ' (💡 THOUGHTFUL SOLVE! +20 XP)' : '')) +
            (hasScratchpadBonus ? ' (✍️ SCRATCHPAD +15 XP)' : '')
          );
          window.MatheduGame.unlockBadge('first_step');
        }

        var eurekaBannerHtml = '';
        if (isDeepEureka) {
          var eBonusScore = 1 + (this.hasRelic('relic_archimedes') ? 2 : 0);
          eurekaBannerHtml = '<div style="margin-bottom:8px;padding:8px 12px;border-radius:10px;background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);border:1.5px solid #f59e0b;color:#78350f;font-size:13px;font-weight:900">' +
            '🧠 <b>[DEEP EUREKA!! 달성]</b> 깊은 사색 끝에 수학적 진리를 스스로 꿰뚫었습니다! (+40 XP · 필살기 +35% · 수능 점수 +' + eBonusScore + '점 추가 상승!)' +
          '</div>';
        } else if (isThoughtfulSolve) {
          eurekaBannerHtml = '<div style="margin-bottom:8px;padding:7px 12px;border-radius:10px;background:#e0f2fe;border:1px solid #38bdf8;color:#0369a1;font-size:12.5px;font-weight:800">' +
            '💡 <b>[THOUGHTFUL SOLVE! 달성]</b> 조건을 차분히 숙고하여 논리적으로 정답을 도출했습니다! (+20 XP 보너스)' +
          '</div>';
        }
        if (hasScratchpadBonus) {
          eurekaBannerHtml += '<div style="margin-bottom:8px;padding:6px 12px;border-radius:10px;background:#f3e8ff;border:1px solid #a855f7;color:#6b21a8;font-size:12px;font-weight:800">' +
            '✍️ <b>[DESCARTES SCRATCHPAD BONUS!]</b> 생각 연습장에 직접 식과 보조선을 작성하며 문제를 해결했습니다! (+15 XP 보너스)' +
          '</div>';
        }

        fb.style.background = '#f0fdf4';
        fb.style.border = '1.5px solid #22c55e';
        fb.innerHTML =
          eurekaBannerHtml +
          '<div style="font-size:14px;font-weight:900;color:#15803d;margin-bottom:6px">' +
            partBreakLabel + ' (' + this.state.combo + '연속 콤보' +
            (isCritDerivation ? ' · ⚡ CRITICAL DERIVATION [' + elapsedSec.toFixed(1) + '초]!' : '') +
            (isFever ? ' · 🔥 FEVER RUSH XP ' + feverMult.toFixed(1) + '배!' : '') +
            ' · 총 +' + stepXp + ' XP)' +
          '</div>' +
          '<div style="font-size:13px;color:#1e293b;line-height:1.65;margin-bottom:12px">' + curStep.exp + '</div>' +
          (isLastStep
            ? '<div style="display:flex;flex-direction:column;gap:8px">' +
                '<button type="button" onclick="window.MatheduQuest.completeStageVictory()" style="width:100%;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#059669 0%,#10b981 100%);color:#ffffff;font-size:14px;font-weight:900;cursor:pointer">🎉 [Q.E.D. 총공격 완수!] 보스 코어 완전 격파 & 수능 점수 +' + stg.scoreReward + '점 획득하기 ➔</button>' +
                '<button type="button" onclick="window.MatheduQuest.openPrShareModal(true)" style="width:100%;padding:11px;border-radius:12px;border:1.5px solid #f59e0b;background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);color:#92400e;font-size:13.5px;font-weight:900;cursor:pointer;box-shadow:0 4px 12px rgba(245,158,11,0.22)">📣 친구 도전장 & SNS 인증 공유 (이 3D 보스 결투장 링크 보내기)</button>' +
              '</div>'
            : '<button type="button" onclick="window.MatheduQuest.nextBattleStep()" style="width:100%;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#006398 0%,#2563eb 100%);color:#ffffff;font-size:14px;font-weight:900;cursor:pointer">다음 3D 결계 링 공략으로 진격 (' + (this.activeStepIdx + 2) + '/' + stg.steps.length + ') ➔</button>');
      } else {
        this.stageMistakes = (this.stageMistakes || 0) + 1;
        var isHastyGuess = (elapsedSec <= 2.5);
        var eulerProtected = false;
        if (this.hasRelic('relic_euler') && !this.eulerShieldUsed && (this.state.combo || 0) > 0) {
          this.eulerShieldUsed = true;
          eulerProtected = true;
          this.spawnFloatingText('🌉 EULER BRIDGE! (콤보 초기화 방어)', '#38bdf8');
        } else {
          this.state.combo = 0;
        }

        var wrongUltGain = 20 + (this.hasRelic('relic_bernoulli') ? 15 : 0);
        if (this.hasRelic('relic_bernoulli')) {
          this.state.shieldHp = Math.min(100, (this.state.shieldHp || 80) + 10);
          this.spawnFloatingText('🎲 BERNOULLI TRIAL! (+필살기 ' + wrongUltGain + '%)', '#fbbf24');
        }
        this.state.ultimateGauge = Math.min(100, (this.state.ultimateGauge || 0) + wrongUltGain);
        this.battle3D.shieldFlash = 25;
        this.battle3D.shake = 6;
        saveQuestState(this.state);

        this.playGameSfx('shield');

        if (window.MatheduGame && typeof window.MatheduGame.recordWrongAnswer === 'function') {
          window.MatheduGame.recordWrongAnswer(stg.slug, this.activeStepIdx + 1, stg.bossName);
        }

        var hastyCoachingHtml = isHastyGuess
          ? '<div style="margin-bottom:8px;padding:9px 12px;border-radius:10px;background:#fffbeb;border:1.5px solid #f59e0b;color:#92400e;font-size:13px;font-weight:800">' +
              '🧘 잠깐! 수학은 속도가 아니라 방향입니다. 사색 모드를 켜거나 폴리아 3단계 생각 징검다리로 조건을 먼저 천천히 살펴볼까요?' +
            '</div>'
          : '';

        fb.style.background = '#fef2f2';
        fb.style.border = '1.5px solid #ef4444';
        fb.innerHTML =
          hastyCoachingHtml +
          '<div style="font-size:14px;font-weight:900;color:#b91c1c;margin-bottom:6px">🛡️ [3D 육각 허니컴 디딤돌 방어막 발동!] 충격을 흡수하고 필살기 게이지를 +' + wrongUltGain + '% 충전했습니다!' + (eulerProtected ? ' (🌉 오일러의 성물이 콤보를 보호했습니다!)' : '') + '</div>' +
          '<div style="font-size:13px;color:#1e293b;line-height:1.65">' +
            '<b>👩‍🏫 mathteacher 핵심 코칭:</b> ' + curStep.exp + '<br>' +
            '<span style="color:#0369a1;font-weight:700">위 해설의 정답 번호(' + curStep.answer + '번)를 다시 눌러 보스의 3D 결계를 파쇄하세요!</span>' +
          '</div>';
      }
      typesetMath(fb);
    },

    nextBattleStep: function() {
      if (!this.activeStage) return;
      this.activeStepIdx++;
      this.stepStartTime = Date.now();
      this.stepAttempts = 0;
      this.resetStepContemplation();
      this.renderBattleModal();
    },

    completeStageVictory: function() {
      var stg = this.activeStage;
      if (!stg) return;

      this.playGameSfx('victory');

      var isPerfectInduction = ((this.stageMistakes || 0) === 0);
      var extraCsat = 0;
      if (this.hasRelic('relic_leibniz')) extraCsat += 1;
      if (isPerfectInduction && this.hasConstellationStar('c3_s2')) extraCsat += 1;
      if (this.hasConstellationStar('c4_s3')) extraCsat += 2;

      if (this.state.clearedStages.indexOf(stg.id) === -1) {
        this.state.clearedStages.push(stg.id);
        this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + (stg.scoreReward || 5) + extraCsat);
      } else {
        this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + 2 + extraCsat);
      }

      var curW = this.getWorldById(this.state.activeWorldId);
      if (curW && this.state.emblems.indexOf(curW.emblemId) === -1) {
        var allCleared = curW.stages.every(function(s) {
          return QuestEngine.state.clearedStages.indexOf(s.id) !== -1;
        });
        if (allCleared || stg.id.indexOf('dyn_') === 0) {
          this.state.emblems.push(curW.emblemId);
        }
      }

      saveQuestState(this.state);

      if (window.MatheduGame) {
        var feverThresh = this.getFeverThreshold();
        var feverMult = this.getFeverMultiplier();
        var isFever = (this.state.combo || 0) >= feverThresh;
        var finalXp = Math.round((stg.xpReward || 50) * (isFever ? feverMult : 1.0) * (isPerfectInduction ? 1.25 : 1.0));
        window.MatheduGame.addXP(finalXp, '🏆 [Q.E.D.] ' + stg.bossName + ' 3D 완전 정복!' + (isPerfectInduction ? ' (✨ PERFECT INDUCTION!)' : '') + (isFever ? ' (🔥 FEVER)' : ''));
        window.MatheduGame.unlockBadge('full_clear');
        if (typeof window.MatheduGame.clearWrongAnswer === 'function' && stg.slug) {
          window.MatheduGame.clearWrongAnswer(stg.slug);
        }
        if (typeof window.MatheduGame.fireConfetti === 'function') {
          window.MatheduGame.fireConfetti();
        }
      }

      this.closeBattleModal();
      this.renderConsoleHub();

      // 🃏 아직 해금하지 않은 수학자의 성물이 남아 있다면 보스 격파 보상으로 3택1 성물 드래프트 오픈!
      if ((this.state.unlockedRelics || []).length < MATH_RELICS.length) {
        this.openRelicDraftModal(true);
      }
    },

    closeBattleModal: function() {
      if (this.battle3D.animId) {
        cancelAnimationFrame(this.battle3D.animId);
        this.battle3D.animId = null;
      }
      var m = document.getElementById('matheduQuestBattleModal');
      if (m) m.remove();
    },

    // =========================================================================
    // 📣 [pr 에이전트 전담] 바이럴 친구 도전장 딥링크 자동 소환 & 외부 홍보 공유 허브
    // =========================================================================
    activePrChannel: 'kakao',
    _challengeHandled: false,

    getActiveChallengeTarget: function() {
      if (this.activeStage && this.activeStage.slug) {
        var s = this.activeStage.slug;
        var paramSlug = (s === 'csat26_22') ? 'csat-2026-22' : s;
        return {
          slug: paramSlug,
          bossName: this.activeStage.bossName || '🐉 [공통 22번 대보스] 지수·로그 역함수 대칭의 군주',
          gradeBadge: this.activeStage.gradeBadge || '4점 대보스 · 2026학년도 수능 공통 22번',
          url: 'https://min7014.github.io/mathedu/?challenge=' + encodeURIComponent(paramSlug)
        };
      }
      return {
        slug: 'csat-2026-22',
        bossName: '🐉 [공통 22번 대보스] 지수·로그 역함수 대칭의 군주',
        gradeBadge: '4점 대보스 · 2026학년도 수능 공통 22번',
        url: 'https://min7014.github.io/mathedu/?challenge=csat-2026-22'
      };
    },

    checkUrlChallengeParam: function() {
      if (this._challengeHandled) return;
      var searchStr = window.location.search || '';
      if (!searchStr || searchStr.indexOf('challenge=') === -1) return;

      var challengeRaw = '';
      try {
        var params = new URLSearchParams(searchStr);
        challengeRaw = (params.get('challenge') || '').trim();
      } catch (e) {
        var m = searchStr.match(/[?&]challenge=([^&#]+)/i);
        if (m && m[1]) challengeRaw = decodeURIComponent(m[1]).trim();
      }
      if (!challengeRaw) return;
      this._challengeHandled = true;

      var self = this;
      var rootEl = document.getElementById('matheduQuestConsoleRoot');
      if (rootEl && typeof rootEl.scrollIntoView === 'function') {
        setTimeout(function() {
          try {
            rootEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } catch (err) {
            rootEl.scrollIntoView();
          }
        }, 120);
      }

      var rawLower = challengeRaw.toLowerCase();
      var norm1 = rawLower.replace(/^csat-20(\d\d)-/, 'csat$1_').replace(/-/g, '_');
      var norm2 = rawLower.replace(/-/g, '_');

      var matchedWorld = null;
      var matchedStage = null;
      for (var wi = 0; wi < WORLDS.length; wi++) {
        var stgs = WORLDS[wi].stages || [];
        for (var si = 0; si < stgs.length; si++) {
          var stg = stgs[si];
          var sSlug = (stg.slug || '').toLowerCase();
          var sId = (stg.id || '').toLowerCase();
          if (sSlug === rawLower || sId === rawLower || sSlug === norm1 || sId === norm1 || sSlug === norm2 || sId === norm2) {
            matchedWorld = WORLDS[wi];
            matchedStage = stg;
            break;
          }
        }
        if (matchedStage) break;
      }

      if (matchedStage && matchedWorld) {
        this.state.activeWorldId = matchedWorld.id;
        saveQuestState(this.state);
        this.renderConsoleHub();
        var challengeStage = JSON.parse(JSON.stringify(matchedStage));
        if (challengeStage.gradeBadge.indexOf('친구 도전장') === -1) {
          challengeStage.gradeBadge = '⚔️ [친구 도전장 결투!] ' + challengeStage.gradeBadge;
        }
        setTimeout(function() {
          self.playGameSfx('summon');
          self.startStageBattle(challengeStage);
          self.showPrToast('⚔️ 친구가 보낸 3D 보스 결투장 (' + challengeStage.bossName + ')이 자동 소환되었습니다!');
        }, 260);
        return;
      }

      // WORLDS 기본 스테이지 외 임의의 16,548문항 기출 slug인 경우 샤드 탐색 후 없으면 대표 22번 대보스 즉시 소환
      var basePath = window.location.pathname.indexOf('/board/') !== -1 ? 'archive_shards/' : 'board/archive_shards/';
      fetch(basePath + 'exam_2026.json')
        .then(function(r) { return r.json(); })
        .then(function(data) {
          var probs = (data && data.problems) ? data.problems : {};
          var foundProb = probs[challengeRaw] || probs[norm2];
          if (!foundProb) {
            var keys = Object.keys(probs);
            for (var k = 0; k < keys.length; k++) {
              var p = probs[keys[k]];
              if ((p.slug || '').toLowerCase() === rawLower || (p.standaloneSlug || '').toLowerCase() === rawLower) {
                foundProb = p;
                break;
              }
            }
          }
          if (foundProb) {
            var opts = foundProb.options || ['$1$', '$2$', '$3$', '$4$', '$5$'];
            var ansIdx = parseInt(foundProb.answer || 1, 10);
            var dynStage = {
              id: 'dyn_challenge_' + foundProb.slug,
              slug: foundProb.slug,
              url: foundProb.standaloneSlug ? ('board/' + foundProb.standaloneSlug + '.html') : ('board/archive.html?id=' + encodeURIComponent(foundProb.slug)),
              gradeBadge: '⚔️ [친구 도전장 결투!] ' + (foundProb.examYear || '2026') + '학년도 ' + (foundProb.subject || '수학') + ' ' + (foundProb.qNum || '') + '번',
              bossName: '🔥 [도전장 보스] ' + (foundProb.title || challengeRaw).replace(/^\[.*?\]\s*/, ''),
              scoreReward: parseInt(foundProb.point || '4', 10),
              xpReward: 80,
              symbols: [
                { sym: '⚔️ 친구의 1:1 결투 초대', desc: '친구가 보낸 기출 보스 도전장입니다. 3단계 디딤돌로 3중 결계를 파쇄하세요!' }
              ],
              steps: [
                {
                  stepNum: 1,
                  label: '🌱 1단계 · [외곽 결계 파쇄: 출발 조건 식 (가)]',
                  know: foundProb.s3 || '주어진 조건을 수식으로 옮기는 첫 디딤돌입니다.',
                  stem: (foundProb.s3_q && foundProb.s3_q.stem) ? foundProb.s3_q.stem : ('출발 조건을 수식으로 세울 때 알맞은 것은?<br>' + (foundProb.s3 || foundProb.stem)),
                  options: (foundProb.s3_q && foundProb.s3_q.options) ? foundProb.s3_q.options : opts,
                  answer: (foundProb.s3_q && foundProb.s3_q.answer) ? foundProb.s3_q.answer : ansIdx,
                  exp: (foundProb.s3_q && foundProb.s3_q.exp) ? foundProb.s3_q.exp : (foundProb.s3 || '조건을 정리합니다.')
                },
                {
                  stepNum: 2,
                  label: '🌳 2단계 · [중간 결계 파쇄: 관계식 유도 (나)]',
                  know: foundProb.s4 || '중간 관계식을 유도하는 단계입니다.',
                  stem: (foundProb.s4_q && foundProb.s4_q.stem) ? foundProb.s4_q.stem : ('관계식을 변형하여 정리할 때 알맞은 것은?<br>' + (foundProb.s4 || foundProb.stem)),
                  options: (foundProb.s4_q && foundProb.s4_q.options) ? foundProb.s4_q.options : opts,
                  answer: (foundProb.s4_q && foundProb.s4_q.answer) ? foundProb.s4_q.answer : ansIdx,
                  exp: (foundProb.s4_q && foundProb.s4_q.exp) ? foundProb.s4_q.exp : (foundProb.s4 || '관계식을 결합합니다.')
                },
                {
                  stepNum: 3,
                  label: '💎 3단계 · [보스 코어 격파: 실전 본문항]',
                  know: '1~2단계의 디딤돌을 결합하여 본문항을 격파하세요!',
                  stem: foundProb.stem,
                  options: opts,
                  answer: ansIdx,
                  exp: ((foundProb.exp_lines && foundProb.exp_lines.length) ? foundProb.exp_lines.slice(0, 6).join('<br>') : '정답을 도출했습니다!')
                }
              ]
            };
            self.playGameSfx('summon');
            self.startStageBattle(dynStage);
            self.showPrToast('⚔️ 친구가 보낸 기출 도전장 (' + dynStage.bossName + ')이 자동 소환되었습니다!');
            return;
          }
          throw new Error('fallback');
        })
        .catch(function() {
          var fallbackWorld = WORLDS[4] || WORLDS[0];
          var fallbackStage = JSON.parse(JSON.stringify(fallbackWorld.stages[0]));
          fallbackStage.gradeBadge = '⚔️ [친구 도전장 결투! · ' + challengeRaw + '] ' + fallbackStage.gradeBadge;
          self.state.activeWorldId = fallbackWorld.id;
          saveQuestState(self.state);
          self.renderConsoleHub();
          self.playGameSfx('summon');
          self.startStageBattle(fallbackStage);
          self.showPrToast('⚔️ 친구 도전장 3D 보스 배틀 아레나가 자동 소환되었습니다!');
        });
    },

    getPrChannelCopyText: function(channelId) {
      var st = this.state || {};
      var pctScore = Math.min(100, Math.max(0, st.csatScore || 0));
      var clearedCount = (st.clearedStages || []).length;
      var selfRef = this;
      var relicNames = (st.equippedRelics || []).map(function(rid) {
        var r = selfRef.getRelicById(rid);
        return r ? (r.icon + ' ' + r.name) : '';
      }).filter(Boolean).join(' · ') || '🔮 단델린의 황금 쌍구';
      var chTarget = this.getActiveChallengeTarget();

      if (channelId === 'insta') {
        return (
          '👑 [오늘의 수능 수학 100점 만점 3D 원정대 기록]\n' +
          '🟩🟩🟩 🧠 DEEP EUREKA! (무오답 귀납 추론 클리어)\n' +
          '📊 현재 수능 만점 게이지: ' + pctScore + ' / 100점 (' + clearedCount + '개 보스 격파)\n' +
          '🃏 장착 중인 수학자의 성물: ' + relicNames + '\n' +
          '16,548개 수능·모의고사 기출과 민은기 선생님의 3,400+ 시각적 기하 증명을 무료 3D 게임으로 정복 중 ✨\n' +
          '⚔️ 내 도전장 링크: ' + chTarget.url + '\n' +
          '#수능수학 #수학100점 #공스타그램 #mathedu #수학게임 #기출문제 #지오지브라'
        );
      }
      if (channelId === 'community') {
        return (
          '📌 [무료 사이트 추천] 수능·평가원·교육청 수학 기출 16,548문항을 3D 게임 + 단계별 디딤돌로 푸는 곳 (mathedu)\n\n' +
          '4점 준킬러·킬러 문제 풀다가 막히면 바로 해설지 보면서 자책하곤 했는데,\n' +
          '여기(https://min7014.github.io/mathedu/)는 문제를 바로 못 풀어도:\n' +
          '1) 제0단계 기호 번역기 ➔ 1단계 초등 직관 ➔ 2단계 (가)·(나) 수식 빈칸 추론으로 힌트를 밟아가며 내 손으로 풀게 해주고,\n' +
          '2) 화면 안에 \'데카르트 모눈종이 연습장\'이랑 \'사색 모드(타이머 정지 + 폴리아 3단계 생각 정리)\'가 있어서 진짜 생각하는 힘을 길러줍니다.\n' +
          '3) 100% 영구 무료(광고·로그인 강제 없음)입니다! 제가 방금 격파한 3D 보스 문제 도전장도 남겨봅니다 👇\n' +
          '👉 ' + chTarget.url
        );
      }
      if (channelId === 'teacher') {
        return (
          '📐 [수업 나눔] 3,400+ 동적 기하(GeoGebra) 시각 증명 & 16,548문항 무장벽 디딤돌 퀴즈 플랫폼 \'mathedu\'\n\n' +
          '민은기 선생님의 수학자료실(https://min7014.github.io/)과 연계된 개방형 수학교육 플랫폼(https://min7014.github.io/mathedu/)을 소개합니다.\n' +
          '• 수학 기초가 부족한 학생도 포물선·타원(단델린의 구), 삼각함수, 미적분, 확통 기출을 1단계 초등 직관부터 차근차근 따라가며 스스로 해결할 수 있습니다.\n' +
          '• 교실 전자칠판/태블릿에서 60fps 3D 수학 도형 홀로그램을 360도 돌려보고, 도전장 딥링크로 학생들과 함께 활용할 수 있는 100% 무료 OER 자료실입니다.\n' +
          '🔗 대표 3D 디딤돌 보스 체험 링크: ' + chTarget.url
        );
      }
      if (channelId === 'global') {
        return (
          '🚀 [Open Educational Resource] mathedu: 3,400+ Visual Geometry Proofs & 16,548 Micro-Scaffolded Math Problems in a 60fps 3D Web RPG!\n' +
          '🟩🟩🟩 🧠 DEEP EUREKA! | CSAT Mastery Gauge: ' + pctScore + ' / 100 pts | Relics: ' + relicNames + '\n' +
          'Explore interactive 3D mathematical monuments (Dandelin Spheres, Euler Spirals, Riemann Sums), use the built-in Descartes Scratchpad & Polya\'s 3-Step Deep Contemplation mode, and master calculus, geometry, and probability step by step — 100% free & open.\n' +
          '👉 Direct 3D Boss Challenge: ' + chTarget.url
        );
      }
      // 기본값: 'kakao' (💬 카톡/단톡방 친구 결투장)
      return (
        '🔥 [수능 수학 100점 만점 3D 원정대 도전장!]\n' +
        '🟩🟩🟩 🧠 DEEP EUREKA! (' + chTarget.bossName + ' 격파!)\n' +
        '📊 내 수능 만점 게이지: ' + pctScore + ' / 100점 · 장착 성물: ' + relicNames + '\n' +
        '막혀도 초등 눈높이 3단계 디딤돌과 인게임 모눈종이 연습장으로 끝까지 내 힘으로 풀 수 있어.\n' +
        '너도 이 3D 보스 문제 첫 시도에 깰 수 있는지 지금 바로 도전해봐! 👇\n' +
        '👉 ' + chTarget.url
      );
    },

    openPrShareModal: function(fromBattle) {
      this.playGameSfx('summon');
      injectDesignerStylesheet();

      var existing = document.getElementById('matheduPrShareModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduPrShareModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:100005;background:rgba(4,8,22,0.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:center;padding:14px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      var st = this.state || {};
      var pctScore = Math.min(100, Math.max(0, st.csatScore || 0));
      var clearedCount = (st.clearedStages || []).length;
      var unlockedStarsCount = (st.constellationStars || []).length;
      var selfRef = this;
      var eqRelicsList = (st.equippedRelics || []).map(function(rid) {
        var r = selfRef.getRelicById(rid);
        return r ? (r.icon + ' ' + r.name) : '';
      }).filter(Boolean);
      var relicsDisplay = eqRelicsList.length > 0 ? eqRelicsList.join(' · ') : '🔮 단델린의 황금 쌍구 (기본 성물)';

      var chTarget = this.getActiveChallengeTarget();
      var activeTab = this.activePrChannel || 'kakao';
      var copyText = this.getPrChannelCopyText(activeTab);

      var tabsConfig = [
        { id: 'kakao', label: '💬 카톡/단톡방 친구 결투장' },
        { id: 'insta', label: '📸 인스타/X #공스타그램 인증' },
        { id: 'community', label: '🔥 수만휘·오르비 수험생 추천글' },
        { id: 'teacher', label: '🏫 수학교사·인디스쿨·블로그 나눔글' },
        { id: 'global', label: '🌐 Global Reddit/EdTech 영문 소개' }
      ];

      var tabsHtml = tabsConfig.map(function(t) {
        var isAct = (t.id === activeTab);
        return '<button type="button" class="quest-micro-btn" onclick="window.MatheduQuest.selectPrChannelTab(\'' + t.id + '\')" ' +
          'style="padding:8px 13px;border-radius:11px;border:1.5px solid ' + (isAct ? '#f59e0b' : '#cbd5e1') + ';' +
          'background:' + (isAct ? 'linear-gradient(135deg,#0f172a 0%,#1e293b 100%)' : '#f8fafc') + ';' +
          'color:' + (isAct ? '#fde047' : '#334155') + ';font-size:12px;font-weight:900;cursor:pointer;box-shadow:' + (isAct ? '0 4px 12px rgba(15,23,42,0.22)' : 'none') + '">' +
          t.label +
        '</button>';
      }).join('');

      existing.innerHTML =
        '<div style="width:100%;max-width:740px;background:#ffffff;border-radius:22px;overflow:hidden;box-shadow:0 24px 56px rgba(0,0,0,0.72);border:2px solid #fbbf24;max-height:94vh;display:flex;flex-direction:column">' +
          '<!-- 상단 헤더 -->' +
          '<div style="background:linear-gradient(135deg,#070d1e 0%,#4c1d95 55%,#be185d 100%);color:#ffffff;padding:15px 20px;display:flex;align-items:center;justify-content:space-between;gap:10px">' +
            '<div>' +
              '<div style="font-size:11px;color:#fde047;font-weight:800">📣 pr 에이전트 바이럴 그로스 허브 · mathteacher × gamemaker × designer × pr</div>' +
              '<div style="font-size:17.5px;font-weight:900;margin-top:2px">⚔️ 외부 홍보 & 친구 도전장 딥링크 공유 허브</div>' +
            '</div>' +
            '<button type="button" onclick="window.MatheduQuest.closePrShareModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.18);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
          '</div>' +

          '<!-- 모달 본문 -->' +
          '<div style="padding:18px 22px;overflow-y:auto;flex:1">' +
            '<!-- 🟩 나의 수능 수학 3D 원정대 전적 인증 카드 미리보기 -->' +
            '<div style="margin-bottom:16px;padding:16px 18px;border-radius:16px;background:linear-gradient(135deg,#060b19 0%,#0f172a 60%,#1e1b4b 100%);border:2px solid #38bdf8;color:#ffffff;box-shadow:0 12px 28px rgba(6,11,25,0.35)">' +
              '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-bottom:10px">' +
                '<span style="padding:3px 10px;border-radius:999px;background:rgba(52,211,153,0.2);border:1px solid #34d399;color:#6ee7b7;font-size:11px;font-weight:900">🟩 나의 수능 수학 3D 원정대 전적 인증 카드</span>' +
                '<span style="font-size:11.5px;color:#93c5fd;font-weight:800">' + this.getGradeRankLabel(pctScore) + '</span>' +
              '</div>' +
              '<div style="font-size:19px;font-weight:900;color:#fde047;letter-spacing:0.02em;margin-bottom:6px">' +
                '🟩🟩🟩 🧠 DEEP EUREKA! <span style="font-size:13px;color:#e2e8f0;font-weight:800">· Q.E.D. 3중 수식 결계 완전 파쇄</span>' +
              '</div>' +
              '<div style="font-size:13.5px;font-weight:800;color:#ffffff;margin-bottom:10px">' +
                '🎯 도전장 타깃 보스: <span style="color:#38bdf8">' + chTarget.bossName + '</span> <span style="font-size:11.5px;color:#cbd5e1">(' + chTarget.gradeBadge + ')</span>' +
              '</div>' +
              '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;margin-bottom:12px">' +
                '<div style="padding:8px 11px;border-radius:10px;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.14)">' +
                  '<div style="font-size:10.5px;color:#94a3b8;font-weight:700">수능 만점 게이지</div>' +
                  '<div style="font-size:15px;font-weight:900;color:#fbbf24;margin-top:2px">' + pctScore + ' / 100점</div>' +
                '</div>' +
                '<div style="padding:8px 11px;border-radius:10px;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.14)">' +
                  '<div style="font-size:10.5px;color:#94a3b8;font-weight:700">클리어 스테이지 · 성좌</div>' +
                  '<div style="font-size:14px;font-weight:900;color:#34d399;margin-top:2px">' + clearedCount + '개 보스 격파 · ' + unlockedStarsCount + '/12 ★</div>' +
                '</div>' +
                '<div style="padding:8px 11px;border-radius:10px;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.14)">' +
                  '<div style="font-size:10.5px;color:#94a3b8;font-weight:700">장착 중인 수학자의 성물</div>' +
                  '<div style="font-size:12px;font-weight:800;color:#e2e8f0;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="' + relicsDisplay + '">' + relicsDisplay + '</div>' +
                '</div>' +
              '</div>' +
              '<div style="padding:8px 12px;border-radius:10px;background:rgba(15,23,42,0.85);border:1px dashed #fbbf24;display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap">' +
                '<span style="font-size:11.5px;color:#fde047;font-weight:800;word-break:break-all">🔗 도전장 딥링크: ' + chTarget.url + '</span>' +
                '<span style="font-size:10.5px;color:#93c5fd;font-weight:700">클릭 시 즉시 3D 보스전 자동 소환!</span>' +
              '</div>' +
            '</div>' +

            '<!-- 📋 5대 외부 채널별 맞춤 홍보 문구 탭 -->' +
            '<div style="margin-bottom:8px;font-size:13px;font-weight:900;color:#0f172a">📋 5대 외부 채널별 맞춤 홍보 문구 선택 (탭을 클릭하면 맞춤 홍보글로 즉시 전환됩니다)</div>' +
            '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px">' +
              tabsHtml +
            '</div>' +

            '<!-- 홍보 문구 미리보기 및 직접 편집 가능한 텍스트 영역 -->' +
            '<textarea id="questPrShareTextarea" readonly style="width:100%;height:145px;padding:12px 14px;border-radius:12px;border:1.5px solid #94a3b8;background:#f8fafc;color:#0f172a;font-size:12.5px;font-weight:600;line-height:1.65;resize:vertical;font-family:inherit;box-sizing:border-box">' +
              copyText +
            '</textarea>' +

            '<!-- 원클릭 복사 & 모바일 네이티브 공유 버튼 바 -->' +
            '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px">' +
              '<button type="button" id="btnCopyPrShareText" class="quest-micro-btn" onclick="window.MatheduQuest.copyPrShareText()" ' +
                'style="flex:2;min-width:210px;padding:12px 18px;border-radius:12px;border:none;background:linear-gradient(135deg,#0284c7 0%,#2563eb 100%);color:#ffffff;font-size:14px;font-weight:900;cursor:pointer;box-shadow:0 6px 16px rgba(37,99,235,0.3)">' +
                '📋 원클릭 복사 (홍보 문구 + 도전장 딥링크)' +
              '</button>' +
              '<button type="button" id="btnNativePrShare" class="quest-micro-btn" onclick="window.MatheduQuest.triggerNativeWebShare()" ' +
                'style="flex:1;min-width:170px;padding:12px 16px;border-radius:12px;border:1.5px solid #f59e0b;background:linear-gradient(135deg,#f59e0b 0%,#db2777 100%);color:#ffffff;font-size:13.5px;font-weight:900;cursor:pointer;box-shadow:0 6px 16px rgba(245,158,11,0.28)">' +
                '📲 모바일 공유 (navigator.share)' +
              '</button>' +
            '</div>' +

            '<!-- 복사 완료 인게임 알림 배너 -->' +
            '<div id="questPrCopyFeedbackBanner" style="display:none;margin-top:10px;padding:10px 14px;border-radius:11px;background:#dcfce7;border:1.5px solid #22c55e;color:#14532d;font-size:12.5px;font-weight:900;text-align:center"></div>' +
          '</div>' +
        '</div>';
    },

    selectPrChannelTab: function(channelId) {
      this.activePrChannel = channelId || 'kakao';
      this.playGameSfx('hit');
      this.openPrShareModal();
    },

    copyPrShareText: function() {
      var self = this;
      var ta = document.getElementById('questPrShareTextarea');
      var textToCopy = ta ? ta.value : this.getPrChannelCopyText(this.activePrChannel || 'kakao');
      var msg = '✅ 클립보드에 홍보 문구와 도전장 링크가 복사되었습니다! 친구나 커뮤니티에 붙여넣어 보세요!';

      function onCopied() {
        self.playGameSfx('eureka');
        self.showPrToast(msg);
        var banner = document.getElementById('questPrCopyFeedbackBanner');
        if (banner) {
          banner.style.display = 'block';
          banner.textContent = msg;
        }
        if (window.MatheduGame && typeof window.MatheduGame.addXP === 'function') {
          window.MatheduGame.addXP(20, '📣 바이럴 친구 도전장 & SNS 홍보 문구 공유 (+20 XP)');
        }
      }

      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(textToCopy).then(onCopied).catch(function() {
          self._fallbackCopyText(textToCopy);
          onCopied();
        });
      } else {
        this._fallbackCopyText(textToCopy);
        onCopied();
      }
    },

    _fallbackCopyText: function(text) {
      try {
        var tempTa = document.createElement('textarea');
        tempTa.value = text;
        tempTa.style.cssText = 'position:fixed;left:-9999px;top:-9999px';
        document.body.appendChild(tempTa);
        tempTa.focus();
        tempTa.select();
        document.execCommand('copy');
        tempTa.remove();
      } catch (e) {}
    },

    triggerNativeWebShare: function() {
      var self = this;
      var chTarget = this.getActiveChallengeTarget();
      var textToShare = this.getPrChannelCopyText(this.activePrChannel || 'kakao');
      if (navigator.share && typeof navigator.share === 'function') {
        this.playGameSfx('eureka');
        navigator.share({
          title: '👑 수능 수학 100점 만점 3D 원정대 도전장 (mathedu)',
          text: textToShare,
          url: chTarget.url
        }).then(function() {
          self.showPrToast('✅ 모바일 공유 시트를 통해 친구에게 도전장을 전송했습니다!');
        }).catch(function() {});
      } else {
        this.copyPrShareText();
      }
    },

    showPrToast: function(message) {
      var existing = document.getElementById('matheduPrViralToast');
      if (existing) existing.remove();
      var toast = document.createElement('div');
      toast.id = 'matheduPrViralToast';
      toast.style.cssText =
        'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:100020;' +
        'background:linear-gradient(135deg,#064e3b 0%,#0f172a 100%);color:#ffffff;' +
        'border:2px solid #34d399;border-radius:999px;padding:11px 22px;font-size:13px;font-weight:900;' +
        'box-shadow:0 12px 32px rgba(0,0,0,0.55);text-align:center;max-width:92vw';
      toast.textContent = message;
      document.body.appendChild(toast);
      setTimeout(function() {
        if (toast && toast.parentNode) toast.remove();
      }, 4200);
    },

    closePrShareModal: function() {
      var m = document.getElementById('matheduPrShareModal');
      if (m) m.remove();
    },

    grantSponsorAdReward: function() {
      this.state.ultimateGauge = 100;
      this.state.shieldHp = 100;
      this.insightGauge = Math.min(100, (this.insightGauge || 0) + 40);
      saveQuestState(this.state);
      this.playGameSfx('victory');
      this.updateInsightGaugeDOM();
      this.renderConsoleHub();
      var battleModal = document.getElementById('matheduQuestBattleModal');
      if (battleModal && this.activeStage) {
        this.renderBattleModal();
      }
      this.showPrToast('🎁 스폰서 광고 시청 보상 수령 완료! (+50 XP · 기하 필살기 100% 완충 · 사색 통찰 +40%)');
    }
  };

  window.MatheduQuest = QuestEngine;
  window.MatheduQuestGame = QuestEngine;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      QuestEngine.renderConsoleHub();
      QuestEngine.checkUrlChallengeParam();
    });
  } else {
    QuestEngine.renderConsoleHub();
    QuestEngine.checkUrlChallengeParam();
  }
})(window);
