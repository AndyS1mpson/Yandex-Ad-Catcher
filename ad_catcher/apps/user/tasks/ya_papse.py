from typing import List, Union
from ad_catcher.celery_app import celery_app
from celery.utils.log import get_task_logger
from scraper.items import BaseBanner, YaBanner
from ad_catcher.settings import YANDEX_PARSE_QUEUE, SAVE_YA_RESULTS_QUQUE
from scraper.spiders.yandex import YaSpider
from apps.user.models import PageUrl, ParseJob, Banner
from datetime import datetime
from scraper.items import YaBanner

logger = get_task_logger(__name__)


@celery_app.task(
    queue=YANDEX_PARSE_QUEUE,
    name='parse',
    soft_time_limit=120
)
def parse(job_id: int, url: str) -> None:
    try:
        ya = YaSpider()

        results = ya.parse(url)
        logger.info("STOP PARSING")
        save_ya_results.s(job_id, results)()
    except Exception:
        parse_job: ParseJob = ParseJob.objects.get(id=job_id)
        parse_job.status = "FAILED"
        parse_job.end_parse = datetime.now()
        parse_job.save()


@celery_app.task(
    queue=SAVE_YA_RESULTS_QUQUE,
    name="save_ya"
)
def save_ya_results(parse_job_id: int, results: List[Union[BaseBanner, YaBanner]]):
    # Update parse job
    logger.info("START SAVING TO DB")
    parse_job: ParseJob = ParseJob.objects.get(id=parse_job_id)
    parse_job.status = "COMPLETE"
    parse_job.end_parse = datetime.now()
    parse_job.save()

    page_res = next((x for x in results if x.name == "page"), None)
    results.remove(page_res)
    page: PageUrl = PageUrl.objects.create(
        full_page=page_res.full_page_path,
        job=parse_job
    )

    # Save results
    # TODO: при каждом создании будет запрос в бд
    # это плохо, но рефакторинг потом
    for res in results:
        banner: Banner = Banner.objects.create(
            file=res.banner_path,
            click_url=res.click_url,
            image_url=res.img_url,
            pageurl=page
        )

