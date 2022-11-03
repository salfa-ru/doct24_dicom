Файлы исследований помещают в папку ./data/{id}/ обязательно в одним из трех способов:

1. Файлы DICOM  - в папку ./data/{id}/dicom/. Среди них обязательно делжн быть файл вида *0001.dcm
2. Файлы DICOM в архиве должны быть переименованы в dicom.zip (./data/{id}/dicom.zip).
3. Файлы NIFIT должны быть переименованы в imaging.nii или imaging.nii.gz

Инициализаци выполняется командой:

ai.processor.LungsAnalyzer(id, segmentation=True)

Параметр segmentation определяет необходимо ли выполнить разметку сегментов легких (по умолчанию segmentation=True).
Разметка сегментов хранится в файле ./data/{id}/segmentation.nii.gz. При повторной инициализации с параметром segmentation=True 
данные загружаются из этого файла, если он имеется.

Разметка COVID запускается командой 

ai.processor.LungsAnalyzer.get_mask(model='covid')

Разметка COVID хранится в файле ./data/{id}/masks/covid.nii.gz.
