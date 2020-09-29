#test species id boxes
import pytest
import os
from DeepTreeAttention.generators import boxes

#random label predictions just for testing
test_predictions = "data/raw/2019_BART_5_320000_4881000_image.shp"

#Use a small rgb crop as a example tile
test_sensor_tile = "data/raw/2019_BART_5_320000_4881000_image_crop.tif"

@pytest.mark.parametrize("train",[True, False])
def test_generate_tfrecords(train, tmpdir):
    
    created_records = boxes.generate_tfrecords(
        shapefile=test_predictions,
        site = 1,
        elevation=100,
        savedir=tmpdir,
        train=train,
        sensor_path=test_sensor_tile,
        species_label_dict=None,
        height=20,
        width=20,
        classes=6)
    
    assert all([os.path.exists(x) for x in created_records])
    
    if train:
        dataset = boxes.tf_dataset(created_records, batch_size=2, mode="train")
    else:
        dataset = boxes.tf_dataset(created_records, batch_size=2, mode="predict")
    
    if train:
        for (image_batch, metadata_batch), label_batch in dataset.take(3):
            assert image_batch.shape == (2,20,20,3)
            assert label_batch.shape == (2,6)
            assert not sum(metadata_batch) == 0            
    else:
        for (image_batch, metadata_batch), box_index_batch in dataset.take(3):
            assert image_batch.shape == (2,20,20,3)
            assert box_index_batch.shape == (2,)
            assert not sum(metadata_batch) == 0
