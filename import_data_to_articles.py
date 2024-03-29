import os
import django
from django.core.files import File
from django.core.files.images import ImageFile

# DJANGO_SETTINGS_MODULE 환경 변수를 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Renaissance.settings")

# Django 설정을 로드
django.setup()

import pandas as pd
from datetime import datetime
from articleapp.models import Article
from projectapp.models import Project
from artistapp.models import Artist, Subtitle
from django.contrib.auth.models import User

def import_data_to_articles(file_path):
    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        title = row['Title']
        content = row['Content']

        # 동일한 title과 content를 가진 article이 이미 존재하는지 확인
        existing_article = Article.objects.filter(title=title, content=content).first()
        if existing_article:
            print(f"Title이 '{title}'인 Article은 이미 존재합니다. 생성을 건너뜁니다.")
            continue

        date_str = row['Date']
        content = row['Content']
        image_path = row['Image']  # 이미지 파일의 경로

        # 날짜 문자열을 datetime 객체로 변환
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # 사용자를 임의로 선택하거나 고정할 수 있습니다.
        # 두 번째 사용자 선택
        user = User.objects.all()[1]

        # Article 모델에 데이터 저장
        article = Article.objects.create(
            writer=user,
            title=title,
            content=content,
            date=date,
            # 다른 필드들도 추가
        )

        # 프로젝트를 추가하려면 해당 필드들의 데이터를 가져와서 추가합니다.
        project_names = row['Project'].split(',')
        projects = []
        for name in project_names:
            # 기본 이미지와 기본 텍스트, 기본 주소를 설정하여 프로젝트 생성
            project, created = Project.objects.get_or_create(
                title=name,
                defaults={'image': 'defalt_image/defalt_stage.jpg', 'description': '설명을 추가해 주세요', 'address': '서울 마포구 독막로 지하 85', 'writer': user}
            )
            projects.append(project)

        article.project.set(projects)

        # 아티스트를 추가하려면 해당 필드들의 데이터를 가져와서 추가합니다.
        artist_names = [name.strip() for name in row['Artist'].split(',')]  # 여기서 공백 제거
        artists = []
        for name in artist_names:
            subtitles = [name]  # Subtitle로 아티스트 이름을 사용
            artist, created = Artist.objects.get_or_create_artist_by_subtitles(
                name,
                subtitles,
                defaults={
                    'image': 'defalt_image/defalt_rockband.jpg',
                    'description': '설명을 추가해 주세요',
                    'writer': user
                }
            )

            # 아티스트에 Subtitle 추가 (이미 추가된 경우에는 중복되지 않음)
            for subtitle_name in subtitles:
                subtitle, _ = Subtitle.objects.get_or_create(name=subtitle_name)
                artist.sub_titles.add(subtitle)

            artists.append(artist)

            # Debug 출력
            print(f"Subtitle: {subtitle.name}, Artist: {artist.title}, Created: {created}")

        article.artist.set(artists)

        # 이미지 파일 등록
        if image_path:
            with open(image_path, 'rb') as image_file:
                article.image.save(os.path.basename(image_path), File(image_file))

# 파일 경로 설정
file_path = 'articleapp/mydata/output20.csv'  # 본인의 데이터 파일 경로로 변경
import_data_to_articles(file_path)
