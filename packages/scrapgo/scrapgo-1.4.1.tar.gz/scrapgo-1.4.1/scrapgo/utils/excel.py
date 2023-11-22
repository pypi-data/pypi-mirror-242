from listorm import write_excel, read_excel, values, asvalues, select




class ExcelFeedMixin:
    excel_feed_excel_path = None
    excel_feed_sheet_name = None
    excel_feed_unique_keys = None
    excel_feed_feed_size = 1000
    excel_feed_feed_mode = 'append'
    excel_feed_action_name = 'exhibitors_detail'
    excel_feed_image_fields = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excel_feed_exists_unique_values = []
        self.excel_feed_records_buffer = []

        if self.excel_feed_excel_path:
            if not self.excel_feed_action_name:
                raise NotImplementedError('Excel Feed Mixin excel_feed_excel_path and excel_feed_action_name must be assigned')
            self.__load_excel()

    def __load_excel(self):
        exsists_records = read_excel(self.excel_feed_excel_path)
        if self.excel_feed_unique_keys:
            self.excel_feed_exists_unique_values = values(exsists_records, keys=self.excel_feed_unique_keys)
    
    def __feed_excel(self, records):
        if self.excel_feed_exists_unique_values:
            records = select(records,
                where=lambda **row: asvalues(row, self.excel_feed_unique_keys) not in self.excel_feed_exists_unique_values
            )
        if records:
            print(f'ExcelFeedMixin: feed {len(records)} records to {self.excel_feed_excel_path}...')
            write_excel(
                records, self.excel_feed_excel_path, self.excel_feed_sheet_name,
                mode=self.excel_feed_feed_mode,
                image_fields=self.excel_feed_image_fields
            )

    def crawl(self, *args, **kwargs):
        super().crawl(*args, **kwargs)
        if composed_buffer := kwargs.get('_composed_buffer'):
            if records_buffer := composed_buffer.get(self.excel_feed_action_name):
                buffed_size = len(records_buffer)
                self.excel_feed_records_buffer = records_buffer
                if buffed_size >= self.excel_feed_feed_size:
                    self.__feed_excel(self.excel_feed_records_buffer)
                    composed_buffer[self.excel_feed_action_name] = []
        
        # 마지막 남은 자투리 마무리
            if len(args) == 0:
                self.__feed_excel(self.excel_feed_records_buffer)
    
    # ctrl+c로 종료시 자투리 마무리
    def __del__(self):
        self.__feed_excel(self.excel_feed_records_buffer)