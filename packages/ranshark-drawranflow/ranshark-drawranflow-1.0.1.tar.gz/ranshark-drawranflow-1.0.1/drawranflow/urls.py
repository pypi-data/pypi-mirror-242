from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # File upload and checking the existence and refresh it if required.
    path('upload/', views.upload, name='upload'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete'),
    path('process_item/<int:item_id>', views.process_item, name='process'),

    path('get_updated_table_data/', views.get_updated_table_data, name='get_updated_table_data'),
    path('check_file_existence/', views.check_file_existence, name='check_file_existence'),

   # path('upload_file/check_file_existence/', views.check_file_existence, name='check_file_existence'),

    # Display processed calls
    path('display-streaming-table/<int:id>', views.display_streaming_table, name='display_streaming_table'),
    path('display-streaming-table/streaming-table-view/', views.streaming_table_view, name='streaming_table_view'),
    path('display-streaming-table/fetch-associated-data/<int:main_id>/', views.fetch_associated_data, name='fetch_associated_data'),
    path('display-streaming-table/draw-sequence/<int:main_id>/', views.draw_sequence_view, name='draw_sequence_view'),
    path('display-streaming-table/draw-sequence/prepare-download-pcap/', views.prepare_download_pcap, name='prepare_download_pcap'),
    path('display-streaming-table/draw-sequence/fetch-packet-data/', views.fetch_packet_data,
         name='fetch-packet-data'),

    path('show-stats/<int:id>', views.show_stats, name='show-stats'),

]


