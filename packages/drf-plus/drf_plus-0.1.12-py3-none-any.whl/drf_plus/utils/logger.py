class QueryLogger:
    """
    특정 범위 쿼리를 확인

    [ 사용 방법 ]
    from django.db import connection
    from base.tests import QueryLogger

    ql = QueryLogger(is_print=True)
    with connection.execute_wrapper(ql):
        # wrapping 할 범위 선택
        pass
    queries = ql.queries
    queries = sorted(queries, key=lambda x: x["duration"], reverse=True)
    print("▶️ 쿼리 수 : ", len(queries), "개")
    print("▶️ 가장 오래 걸린 쿼리 :\n", queries[0]["sql"])
    print("▶️ 총 소요 시간 : ", ql.total_duration, "ms")
    print("▶️ 중복 쿼리 수 : ", queries[0]["duplicate_query"], "개")
    """

    def __init__(self, is_print: bool = False):
        self.queries = []
        self.sql_list = []
        self.total_duration = 0
        # 바로 표시할지 여부 확인
        self.is_print = is_print

    def __call__(self, execute, sql, params, many, context):
        import time

        current_query = {"sql": sql, "params": params, "many": many}

        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            current_query["status"] = "error"
            current_query["exception"] = e
            raise
        else:
            current_query["status"] = "ok"
            return result
        finally:
            # 수행 시간
            duration = time.monotonic() - start

            duration_ms = duration * 1000
            current_query["duration"] = duration_ms
            # 총 수행시간
            self.total_duration += duration_ms
            current_query["total_duration"] = self.total_duration

            self.sql_list.append(current_query["sql"])
            current_query["sql_count"] = len(self.sql_list)
            from collections import Counter

            result = Counter(self.sql_list)
            for key, value in result.items():
                if value >= 2:
                    current_query["duplicate_query"] = value

            if self.is_print:
                # 바로 표시
                print(current_query)
                self.queries.append(current_query)
            else:
                # 배열에 저장
                self.queries.append(current_query)


class QueryLoggerDecorator:
    """
    특정 범위 쿼리를 확인 - 데코레이터

    [ 사용 방법 ]
    @QueryLoggerDecorator(is_print=True)
    def ...(...):
        pass
    """

    def __init__(self, is_print: bool = False):
        self.is_print = is_print

    def __call__(self, func):
        def inner(*args, **kwargs):
            from django.db import connection

            ql = QueryLogger(is_print=self.is_print)
            with connection.execute_wrapper(ql):
                func(*args, **kwargs)
            if not self.is_print:
                queries = ql.queries
                queries = sorted(queries, key=lambda x: x["duration"], reverse=True)
                print("🧾 함수명\n => ", func.__name__)
                print("▶️ 쿼리 수 : ", len(queries), "개")
                print("▶️ 가장 오래 걸린 쿼리 :\n", queries[0]["sql"])
                print("▶️ 총 소요 시간 : ", ql.total_duration, "ms")
                print("▶️ 중복 쿼리 수 : ", queries[0]["duplicate_query"], "개")
        return inner
