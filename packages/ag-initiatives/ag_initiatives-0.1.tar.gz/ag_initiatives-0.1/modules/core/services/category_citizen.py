import os
from redis import Redis
import datetime


class CategoryCitizenRedisService:

    def __init__(self):
        self.redis_instance = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT', '6379'),
            db=10
        )

    def _citizen_exists_in_db(self, user_id):
        return self.redis_instance.exists(user_id)

    def _get_ttl_of_citizen(self, user_id):
        return self.redis_instance.ttl(user_id)

    def _transform_ttl_to_datetime(self, ttl):
        return datetime.timedelta(seconds=ttl)

    def _update_citizen_value_in_db(self, user_id):
        value = self.get_count_of_changes(user_id)
        if not value:
            self._put_citizen_with_first_value_in_db(user_id)
        if value == b'1':
            ttl = self._get_ttl_of_citizen(user_id)
            self._put_citizen_with_second_value_in_db(user_id, ttl)
        return value

    def _put_citizen_with_second_value_in_db(self, user_id, ttl):
        self.redis_instance.set(
            name=user_id,
            value=2,
            ex=ttl
        )

    def _put_citizen_with_first_value_in_db(self, user_id):
        self.redis_instance.set(
            name=user_id,
            value=1,
            ex=60 * 60 * 24 * 30,  # 30 суток
        )

    def get_time_left(self, user_id):
        time_left_seconds = self._get_ttl_of_citizen(user_id)
        if time_left_seconds < 0:
            return 0
        time_left = self._transform_ttl_to_datetime(time_left_seconds)
        return str(time_left)

    def get_count_of_changes(self, user_id):
        return self.redis_instance.get(user_id)

    def set_restriction_of_changes(self, user_id):
        values = {
            None: "Made the first change",
            b'1': "Made the second change",
            b'2': "Changes are no longer available"
        }
        value = self._update_citizen_value_in_db(user_id)
        time_left = self.get_time_left(user_id)
        return {values[value]: time_left}


category_citizen_redis = CategoryCitizenRedisService()
