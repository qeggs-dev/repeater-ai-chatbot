def main(run_server: bool = True):
    while True:
        import time
        start_import_time = time.perf_counter_ns()
        import sys
        from core import RepeaterMain
        from loguru import logger
        end_import_time = time.perf_counter_ns()

        repeater_main = RepeaterMain()

        load_configs_start_time = time.perf_counter_ns()
        configs = repeater_main.load_configs()
        load_configs_end_time = time.perf_counter_ns()

        logger_init_start_time = time.perf_counter_ns()
        repeater_main.init_logger()
        logger_init_end_time = time.perf_counter_ns()

        logger.info(
            "Import Packages Time: {import_packages_time:.2f}ms",
            import_packages_time = (end_import_time - start_import_time) / 1e6
        )
        logger.info(
            "Init Logger Time: {logger_init_time:.2f}ms",
            logger_init_time = (logger_init_end_time - logger_init_start_time) / 1e6
        )
        logger.info(
            "Load Configs Time: {load_configs_time:.2f}ms",
            load_configs_time = (load_configs_end_time - load_configs_start_time) / 1e6
        )

        if run_server is None:
            run_server = configs.server.run_server
        
        repeater_main.init_all(configs)
        repeater_main.init_server(configs)
        
        if run_server:
            exit_code = repeater_main.run()
        
        if exit_code != 0:
            logger.error(
                "Repeater exited with code {exit_code}",
                exit_code = exit_code
            )
            sys.exit(exit_code)
        
        if configs.server.restart:
            logger.info("Repeater Restarting...")
        else:
            break

if __name__ == "__main__":
    main()