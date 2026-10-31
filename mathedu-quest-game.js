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

  function loadQuestState() {
    try {
      var raw = localStorage.getItem(QUEST_STATE_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        return {
          csatScore: typeof parsed.csatScore === 'number' ? parsed.csatScore : 0,
          clearedStages: Array.isArray(parsed.clearedStages) ? parsed.clearedStages : [],
          emblems: Array.isArray(parsed.emblems) ? parsed.emblems : [],
          combo: typeof parsed.combo === 'number' ? parsed.combo : 0,
          shieldHp: typeof parsed.shieldHp === 'number' ? parsed.shieldHp : 100,
          activeWorldId: parsed.activeWorldId || 'w1',
          summonedCount: parsed.summonedCount || 0
        };
      }
    } catch (e) {}
    return {
      csatScore: 0,
      clearedStages: [],
      emblems: [],
      combo: 0,
      shieldHp: 100,
      activeWorldId: 'w1',
      summonedCount: 0
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

  var QuestEngine = {
    state: loadQuestState(),
    activeStage: null,
    activeStepIdx: 0,
    shardCache: {},

    getWorlds: function() {
      return WORLDS;
    },

    getWorldById: function(wid) {
      for (var i = 0; i < WORLDS.length; i++) {
        if (WORLDS[i].id === wid) return WORLDS[i];
      }
      return WORLDS[0];
    },

    getGradeRankLabel: function(score) {
      if (score >= 100) return '👑 수능 수학 100점 만점 (전국 수석 마스터)';
      if (score >= 92) return '💎 1등급 최상위권 (' + score + '점 / 100점)';
      if (score >= 84) return '🔥 1등급 진입권 (' + score + '점 / 100점)';
      if (score >= 74) return '⚡ 공통과목 마스터권 (' + score + '점 / 100점)';
      if (score >= 45) return '🌿 중위권 도약 중 (' + score + '점 / 100점)';
      return '🌱 기초 디딤돌 등반 중 (' + score + '점 / 100점)';
    },

    selectWorld: function(wid) {
      this.state.activeWorldId = wid;
      saveQuestState(this.state);
      this.renderConsoleHub();
    },

    startStageBattle: function(stageObj) {
      if (!stageObj) return;
      this.activeStage = stageObj;
      this.activeStepIdx = 0;
      this.renderBattleModal();
    },

    startStageById: function(worldId, stageId) {
      var w = this.getWorldById(worldId);
      if (!w) return;
      for (var i = 0; i < w.stages.length; i++) {
        if (w.stages[i].id === stageId) {
          this.startStageBattle(w.stages[i]);
          return;
        }
      }
    },

    // 16,548문항 연도별 샤드 DB에서 실시간으로 해당 대륙 기출 보스 소환!
    summonRandomArchiveProblem: function(worldId) {
      var self = this;
      var w = this.getWorldById(worldId || this.state.activeWorldId);
      var years = w.shardYears || ['2025'];
      var pickYear = years[Math.floor(Math.random() * years.length)];
      var basePath = window.location.pathname.indexOf('/board/') !== -1 ? 'archive_shards/' : 'board/archive_shards/';
      var shardUrl = basePath + 'exam_' + pickYear + '.json';

      var btn = document.getElementById('btnSummonArchiveBoss');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '⏳ 16,548문항 아카이브에서 맞춤형 기출 보스 소환 중...';
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
          gradeBadge: '🎲 실시간 기출 소환 · ' + prob.examYear + '학년도 ' + prob.month + ' ' + prob.grade + ' ' + prob.subject + ' ' + prob.qNum + '번 (' + (prob.point || '3') + '점)',
          bossName: '👾 [' + leafUnit + '] ' + prob.title.replace(/^\[.*?\]\s*/, ''),
          scoreReward: parseInt(prob.point || '3', 10),
          xpReward: 50,
          symbols: [
            { sym: '📌 핵심 단원: ' + leafUnit, desc: (prob.intent || (leafUnit + '의 정의와 성질을 적용하는 실전 기출문항입니다.')) },
            { sym: '🎯 배점 및 번호: ' + prob.qNum + '번 (' + (prob.point || '3') + '점)', desc: '초등 디딤돌부터 출발 식(가) ➔ 중간 유도식(나) ➔ 본문항 순서로 격파하세요!' }
          ],
          steps: [
            {
              stepNum: 1,
              label: '🌱 1단계 · [출발 조건 식 세우기 (가)] ' + leafUnit,
              know: '문제의 출발 조건을 수식으로 옮기는 첫 디딤돌입니다.<br>• <b>핵심 단서</b>: ' + (prob.s3 || leafUnit),
              stem: s3Q.stem,
              options: s3Q.options,
              answer: s3Q.answer,
              exp: s3Q.exp
            },
            {
              stepNum: 2,
              label: '🌳 2단계 · [중간 관계식 유도 (나)] ' + leafUnit,
              know: '출발 식을 변형하여 목표값에 다가가는 중간 유도 단계입니다.<br>• <b>핵심 전개</b>: ' + (prob.s4 || leafUnit),
              stem: s4Q.stem,
              options: s4Q.options,
              answer: s4Q.answer,
              exp: s4Q.exp
            },
            {
              stepNum: 3,
              label: '💎 3단계 · [실전 기출 본문항 격파] ' + prob.examYear + '학년도 ' + prob.qNum + '번',
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
          btn.innerHTML = '🎲 이 대륙의 기출 보스 무작위 소환 (16,548문항 DB)';
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
            btn.innerHTML = '🎲 이 대륙의 기출 보스 무작위 소환 (16,548문항 DB)';
          }
          pickFromShardData(data);
        })
        .catch(function() {
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🎲 이 대륙의 기출 보스 무작위 소환 (16,548문항 DB)';
          }
          if (w.stages && w.stages.length) {
            self.startStageBattle(w.stages[0]);
          }
        });
    },

    summonMin7014Grimoire: function(url) {
      this.state.shieldHp = 100;
      saveQuestState(this.state);
      if (window.MatheduGame && typeof window.MatheduGame.unlockBadge === 'function') {
        window.MatheduGame.unlockBadge('min7014_explorer');
        window.MatheduGame.addXP(15, '📐 민은기 선생님 시각 증명 비급서 탐구 (+보호막 100% 충전)');
      }
      var hpEl = document.getElementById('questBattleShieldText');
      if (hpEl) hpEl.textContent = '100%';
      if (url) {
        window.open(url, '_blank', 'noopener');
      }
    },

    renderConsoleHub: function() {
      var container = document.getElementById('matheduQuestConsoleRoot');
      if (!container) return;

      var st = this.state;
      var activeW = this.getWorldById(st.activeWorldId);
      var pctScore = Math.min(100, Math.max(0, st.csatScore));

      var worldTabsHtml = WORLDS.map(function(w) {
        var isAct = (w.id === activeW.id);
        var hasEmblem = st.emblems.indexOf(w.emblemId) !== -1;
        return '<button type="button" onclick="window.MatheduQuest.selectWorld(\'' + w.id + '\')" ' +
          'style="padding:8px 12px;border-radius:12px;border:1.5px solid ' + (isAct ? '#006398' : '#e2e8f0') + ';' +
          'background:' + (isAct ? 'linear-gradient(135deg,#006398 0%,#0284c7 100%)' : '#ffffff') + ';' +
          'color:' + (isAct ? '#ffffff' : '#1e293b') + ';font-size:12px;font-weight:800;cursor:pointer;display:inline-flex;align-items:center;gap:5px;transition:all .15s;box-shadow:' + (isAct ? '0 4px 12px rgba(0,99,152,0.25)' : 'none') + '">' +
          '<span>' + w.icon + ' World ' + w.num + '</span>' +
          (hasEmblem ? '<span title="대륙 정복 완료">✅</span>' : '') +
        '</button>';
      }).join('');

      var stagesHtml = activeW.stages.map(function(stg) {
        var isCleared = st.clearedStages.indexOf(stg.id) !== -1;
        return '<div style="padding:14px 16px;border-radius:14px;background:' + (isCleared ? '#f0fdf4' : '#ffffff') + ';border:1.5px solid ' + (isCleared ? '#86efac' : '#cbd5e1') + ';display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;box-shadow:0 2px 8px rgba(15,23,42,0.04)">' +
          '<div style="flex:1;min-width:210px">' +
            '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:4px">' +
              '<span style="padding:2px 8px;border-radius:999px;background:#e0f2fe;color:#0369a1;font-size:10.5px;font-weight:800">' + stg.gradeBadge + '</span>' +
              '<span style="padding:2px 8px;border-radius:999px;background:#fef3c7;color:#b45309;font-size:10.5px;font-weight:800">수능 +' + stg.scoreReward + '점 · +' + stg.xpReward + ' XP</span>' +
              (isCleared ? '<span style="padding:2px 8px;border-radius:999px;background:#dcfce7;color:#15803d;font-size:10.5px;font-weight:800">✅ 격파 완료</span>' : '') +
            '</div>' +
            '<div style="font-size:14.5px;font-weight:800;color:#0f172a">' + stg.bossName + '</div>' +
          '</div>' +
          '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">' +
            '<button type="button" onclick="window.MatheduQuest.startStageById(\'' + activeW.id + '\',\'' + stg.id + '\')" ' +
              'style="padding:8px 14px;border-radius:10px;border:none;background:linear-gradient(135deg,#006398 0%,#2563eb 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 2px 8px rgba(37,99,235,0.25)">' +
              '⚔️ 인게임 단계별 전투 시작' +
            '</button>' +
            '<a href="' + stg.url + '" style="padding:8px 11px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc;color:#334155;font-size:11.5px;font-weight:700;text-decoration:none">' +
              '🔎 풀스크린 퀴즈' +
            '</a>' +
          '</div>' +
        '</div>';
      }).join('');

      var minLinksHtml = (activeW.min7014Links || []).map(function(ml) {
        return '<button type="button" onclick="window.MatheduQuest.summonMin7014Grimoire(\'' + ml.url + '\')" ' +
          'style="padding:6px 11px;border-radius:999px;border:1px solid #bae6fd;background:#f0f9ff;color:#0369a1;font-size:11.5px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:4px">' +
          '<span>🔮 ' + ml.title + '</span>' +
          '<span style="font-size:10px;background:#0284c7;color:#fff;padding:1px 6px;border-radius:999px">+보호막 충전</span>' +
        '</button>';
      }).join('');

      var emblemsBar = WORLDS.map(function(w) {
        var unlocked = st.emblems.indexOf(w.emblemId) !== -1;
        return '<span style="padding:3px 9px;border-radius:999px;font-size:11px;font-weight:700;' +
          (unlocked ? 'background:#fef3c7;color:#92400e;border:1px solid #f59e0b' : 'background:#f1f5f9;color:#94a3b8;border:1px dashed #cbd5e1') + '">' +
          w.emblemName + (unlocked ? ' ✨' : ' (미획득)') +
        '</span>';
      }).join('');

      container.innerHTML =
        '<div style="border-radius:18px;background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%);padding:18px;color:#ffffff;box-shadow:0 12px 28px rgba(15,23,42,0.18)">' +
          '<!-- 상단 타이틀 & 수능 100점 만점 게이지 HUD -->' +
          '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px">' +
            '<div>' +
              '<div style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;background:rgba(56,189,248,0.18);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;font-size:11px;font-weight:800;margin-bottom:6px">' +
                '<span>👩‍🏫 mathteacher 에이전트 × 16,548문항 × min7014 시각증명</span>' +
              '</div>' +
              '<h2 style="margin:0;font-size:20px;font-weight:900;letter-spacing:-0.02em;color:#ffffff">👑 수능 수학 100점 만점 원정대 (CSAT 100-Point Quest)</h2>' +
              '<p style="margin:4px 0 0;font-size:12.5px;color:#cbd5e1">초등 눈높이 0~5단계 디딤돌 보호막으로 보스를 격파하며 수능 수학 100점 만점 왕관을 차지하세요!</p>' +
            '</div>' +
            '<div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);border-radius:14px;padding:10px 14px;min-width:220px;text-align:right">' +
              '<div style="font-size:11px;color:#93c5fd;font-weight:700">' + this.getGradeRankLabel(pctScore) + '</div>' +
              '<div style="font-size:22px;font-weight:900;color:#fbbf24;margin:2px 0">' + pctScore + ' <span style="font-size:13px;color:#e2e8f0">/ 100점 만점</span></div>' +
              '<div style="width:100%;height:8px;background:rgba(255,255,255,0.15);border-radius:999px;overflow:hidden">' +
                '<div style="width:' + pctScore + '%;height:100%;background:linear-gradient(90deg,#38bdf8,#fbbf24,#10b981);transition:width .35s ease"></div>' +
              '</div>' +
            '</div>' +
          '</div>' +

          '<!-- 획득한 마스터 엠블럼 컬렉션 -->' +
          '<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:14px;padding:8px 12px;background:rgba(255,255,255,0.05);border-radius:12px">' +
            '<span style="font-size:11.5px;font-weight:800;color:#e2e8f0;margin-right:4px">🏆 정복 엠블럼:</span>' +
            emblemsBar +
          '</div>' +

          '<!-- 6대 대륙 월드맵 탭 -->' +
          '<div style="display:flex;align-items:center;gap:6px;overflow-x:auto;padding-bottom:8px;margin-bottom:12px">' +
            worldTabsHtml +
          '</div>' +

          '<!-- 선택된 대륙 상세 카드 -->' +
          '<div style="background:#f8fafc;color:#0f172a;border-radius:16px;padding:16px">' +
            '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px">' +
              '<div>' +
                '<div style="font-size:16px;font-weight:900;color:#0f172a">' + activeW.icon + ' ' + activeW.name + '</div>' +
                '<div style="font-size:12px;color:#475569;font-weight:600;margin-top:2px">' + activeW.sub + '</div>' +
              '</div>' +
              '<button type="button" id="btnSummonArchiveBoss" onclick="window.MatheduQuest.summonRandomArchiveProblem(\'' + activeW.id + '\')" ' +
                'style="padding:9px 14px;border-radius:12px;border:1.5px solid #7c3aed;background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 100%);color:#ffffff;font-size:12px;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(124,58,237,0.25)">' +
                '🎲 이 대륙의 기출 보스 무작위 소환 (16,548문항 DB)' +
              '</button>' +
            '</div>' +

            '<!-- mathteacher 에이전트 수학 조언 브리핑 -->' +
            '<div style="padding:10px 14px;border-radius:12px;background:#eff6ff;border-left:4px solid #0284c7;font-size:12.5px;color:#1e3a8a;margin-bottom:12px;line-height:1.55">' +
              '<b>👩‍🏫 [mathteacher 수석 교사 브리핑]</b> ' + activeW.teacherAdvice +
            '</div>' +

            '<!-- 스테이지 / 보스 목록 -->' +
            '<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:14px">' +
              stagesHtml +
            '</div>' +

            '<!-- 민은기 선생님(min7014.github.io) 시각 증명 비급서 소환 바 -->' +
            '<div style="padding-top:10px;border-top:1px dashed #cbd5e1;display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
              '<span style="font-size:11.5px;font-weight:800;color:#0369a1">📐 민은기 선생님(min7014.github.io) 시각 증명 비급서:</span>' +
              minLinksHtml +
            '</div>' +
          '</div>' +
        '</div>';

      typesetMath(container);
    },

    renderBattleModal: function() {
      var stg = this.activeStage;
      if (!stg) return;

      var existing = document.getElementById('matheduQuestBattleModal');
      if (!existing) {
        existing = document.createElement('div');
        existing.id = 'matheduQuestBattleModal';
        existing.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(15,23,42,0.84);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;padding:16px;overflow-y:auto';
        document.body.appendChild(existing);
      }

      var totalSteps = stg.steps.length;
      var curStep = stg.steps[this.activeStepIdx] || stg.steps[0];
      var bossHpPct = Math.max(0, Math.round(((totalSteps - this.activeStepIdx) / totalSteps) * 100));

      var symHtml = (stg.symbols || []).map(function(s) {
        return '<div style="padding:6px 10px;background:#ffffff;border:1px solid #bae6fd;border-radius:8px;font-size:12px;color:#0f172a">' +
          '<b>' + s.sym + '</b> — ' + s.desc +
        '</div>';
      }).join('');

      var optsHtml = (curStep.options || []).map(function(opt, i) {
        var optNum = i + 1;
        return '<button type="button" class="quest-battle-opt-btn" onclick="window.MatheduQuest.submitBattleOption(' + optNum + ')" ' +
          'style="width:100%;text-align:left;padding:12px 14px;border-radius:12px;border:1.5px solid #cbd5e1;background:#ffffff;color:#0f172a;font-size:14px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:10px;transition:all .15s">' +
          '<span style="width:26px;height:26px;border-radius:999px;background:#f1f5f9;color:#0f172a;font-weight:800;font-size:12px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0">' + optNum + '</span>' +
          '<span style="flex:1">' + opt + '</span>' +
        '</button>';
      }).join('');

      existing.innerHTML =
        '<div style="width:100%;max-width:680px;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 24px 48px rgba(0,0,0,0.4);border:2px solid #0284c7;max-height:92vh;display:flex;flex-direction:column">' +
          '<!-- 전투 상단 헤더 -->' +
          '<div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 100%);color:#ffffff;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px">' +
            '<div>' +
              '<div style="font-size:11px;color:#38bdf8;font-weight:800">' + stg.gradeBadge + '</div>' +
              '<div style="font-size:17px;font-weight:900;margin-top:2px">' + stg.bossName + '</div>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px">' +
              '<a href="' + stg.url + '" style="padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.15);color:#ffffff;font-size:11.5px;font-weight:700;text-decoration:none">🔎 풀스크린 열기</a>' +
              '<button type="button" onclick="window.MatheduQuest.closeBattleModal()" style="width:32px;height:32px;border-radius:999px;border:none;background:rgba(255,255,255,0.15);color:#ffffff;font-size:16px;font-weight:800;cursor:pointer">✕</button>' +
            '</div>' +
          '</div>' +

          '<!-- 보스 체력 & 디딤돌 보호막 게이지 바 -->' +
          '<div style="background:#f1f5f9;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:1px solid #e2e8f0">' +
            '<div style="flex:1;min-width:180px">' +
              '<div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;color:#b91c1c;margin-bottom:4px">' +
                '<span>👾 보스 수식 장갑 (Armor)</span><span>' + bossHpPct + '% (단계 ' + (this.activeStepIdx + 1) + '/' + totalSteps + ')</span>' +
              '</div>' +
              '<div style="width:100%;height:8px;background:#fee2e2;border-radius:999px;overflow:hidden">' +
                '<div style="width:' + bossHpPct + '%;height:100%;background:linear-gradient(90deg,#ef4444,#f97316);transition:width .3s"></div>' +
              '</div>' +
            '</div>' +
            '<div style="display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;color:#0369a1">' +
              '<span>🛡️ 초등 디딤돌 보호막: <b id="questBattleShieldText">' + this.state.shieldHp + '%</b></span>' +
              '<span>🔥 콤보: <b>' + this.state.combo + '연속</b></span>' +
            '</div>' +
          '</div>' +

          '<!-- 전투 본문 스크롤 영역 -->' +
          '<div style="padding:18px 20px;overflow-y:auto;flex:1">' +
            '<!-- 제0단계 수학 기호 번역기 마법서 -->' +
            '<details style="margin-bottom:14px;background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:10px 14px" open>' +
              '<summary style="font-size:12.5px;font-weight:800;color:#0369a1;cursor:pointer">🔰 [제0단계 기호 번역기 마법서] 낯선 수학 기호 한눈에 번역하기</summary>' +
              '<div style="display:flex;flex-direction:column;gap:6px;margin-top:8px">' + symHtml + '</div>' +
            '</details>' +

            '<!-- 현재 단계 지식 가이드 -->' +
            '<div style="margin-bottom:14px;padding:12px 14px;background:#f8fafc;border-left:4px solid #0284c7;border-radius:10px">' +
              '<div style="font-size:13px;font-weight:900;color:#006398;margin-bottom:4px">' + curStep.label + '</div>' +
              '<div style="font-size:12.5px;color:#334155;line-height:1.6">💡 <b>[mathteacher 디딤돌 힌트]</b> ' + curStep.know + '</div>' +
            '</div>' +

            '<!-- 발문 -->' +
            '<div style="font-size:15px;font-weight:700;color:#0f172a;line-height:1.75;margin-bottom:14px;padding:12px 14px;background:#ffffff;border:1.5px solid #e2e8f0;border-radius:12px">' +
              curStep.stem +
            '</div>' +

            '<!-- 5지선다 버튼 -->' +
            '<div id="questBattleOptsWrap" style="display:flex;flex-direction:column;gap:8px">' +
              optsHtml +
            '</div>' +

            '<!-- 정답/오답 피드백 및 다음 단계 버튼 -->' +
            '<div id="questBattleFeedbackBox" style="display:none;margin-top:14px;padding:14px;border-radius:12px"></div>' +
          '</div>' +
        '</div>';

      typesetMath(existing);
    },

    submitBattleOption: function(chosenIdx) {
      var stg = this.activeStage;
      if (!stg) return;
      var curStep = stg.steps[this.activeStepIdx];
      if (!curStep) return;

      var isCorrect = (chosenIdx === parseInt(curStep.answer, 10));
      var fb = document.getElementById('questBattleFeedbackBox');
      if (!fb) return;

      fb.style.display = 'block';
      if (isCorrect) {
        this.state.combo = (this.state.combo || 0) + 1;
        this.state.shieldHp = Math.min(100, (this.state.shieldHp || 80) + 15);
        saveQuestState(this.state);

        if (window.MatheduGame) {
          window.MatheduGame.recordActivity();
          window.MatheduGame.addXP(15, curStep.label + ' 돌파!');
          window.MatheduGame.unlockBadge('first_step');
        }

        var isLastStep = (this.activeStepIdx >= stg.steps.length - 1);
        fb.style.background = '#f0fdf4';
        fb.style.border = '1.5px solid #22c55e';
        fb.innerHTML =
          '<div style="font-size:14px;font-weight:900;color:#15803d;margin-bottom:6px">🎯 정밀 타격 성공! (' + this.state.combo + '연속 콤보 · 디딤돌 보호막 +15% 회복)</div>' +
          '<div style="font-size:13px;color:#1e293b;line-height:1.65;margin-bottom:12px">' + curStep.exp + '</div>' +
          (isLastStep
            ? '<button type="button" onclick="window.MatheduQuest.completeStageVictory()" style="width:100%;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#059669 0%,#10b981 100%);color:#ffffff;font-size:14px;font-weight:900;cursor:pointer">🎉 보스 최종 격파! 수능 점수 +' + stg.scoreReward + '점 획득하기 ➔</button>'
            : '<button type="button" onclick="window.MatheduQuest.nextBattleStep()" style="width:100%;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#006398 0%,#2563eb 100%);color:#ffffff;font-size:14px;font-weight:900;cursor:pointer">다음 디딤돌 단계로 진격 (' + (this.activeStepIdx + 2) + '/' + stg.steps.length + ') ➔</button>');
      } else {
        this.state.combo = 0;
        saveQuestState(this.state);
        if (window.MatheduGame && typeof window.MatheduGame.recordWrongAnswer === 'function') {
          window.MatheduGame.recordWrongAnswer(stg.slug, this.activeStepIdx + 1, stg.bossName);
        }
        fb.style.background = '#fef2f2';
        fb.style.border = '1.5px solid #ef4444';
        fb.innerHTML =
          '<div style="font-size:14px;font-weight:900;color:#b91c1c;margin-bottom:6px">🛡️ [초등 디딤돌 보호막 발동!] 게임 오버 없이 힌트로 즉시 재도전합니다!</div>' +
          '<div style="font-size:13px;color:#1e293b;line-height:1.65">' +
            '<b>👩‍🏫 mathteacher 핵심 코칭:</b> ' + curStep.exp + '<br>' +
            '<span style="color:#0369a1;font-weight:700">위 해설의 정답 번호(' + curStep.answer + '번)를 다시 눌러 보스의 장갑을 격파하세요!</span>' +
          '</div>';
      }
      typesetMath(fb);
    },

    nextBattleStep: function() {
      if (!this.activeStage) return;
      this.activeStepIdx++;
      this.renderBattleModal();
    },

    completeStageVictory: function() {
      var stg = this.activeStage;
      if (!stg) return;

      if (this.state.clearedStages.indexOf(stg.id) === -1) {
        this.state.clearedStages.push(stg.id);
        this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + (stg.scoreReward || 5));
      } else {
        this.state.csatScore = Math.min(100, (this.state.csatScore || 0) + 2);
      }

      // Check world emblem unlock
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
        window.MatheduGame.addXP(stg.xpReward || 50, '🏆 ' + stg.bossName + ' 완전 정복!');
        window.MatheduGame.unlockBadge('full_clear');
        if (typeof window.MatheduGame.fireConfetti === 'function') {
          window.MatheduGame.fireConfetti();
        }
      }

      this.closeBattleModal();
      this.renderConsoleHub();
    },

    closeBattleModal: function() {
      var m = document.getElementById('matheduQuestBattleModal');
      if (m) m.remove();
    }
  };

  window.MatheduQuest = QuestEngine;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      QuestEngine.renderConsoleHub();
    });
  } else {
    QuestEngine.renderConsoleHub();
  }
})(window);
