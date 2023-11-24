import os
import pandas as pd
import tensorflow as tf


def load():
  exported_path = f'model/{next(os.walk("model"))[1][0]}'
  exported_model = tf.saved_model.load(exported_path)
  serving_default = exported_model.signatures["serving_default"]
  return exported_model, serving_default


class AddressModel:
  def __init__(self, servingDefault, map2Func, encodeTextFunc, addressFunc):
    self.servingDefault = servingDefault
    self.map2Func = map2Func
    self.encodeTextFunc = encodeTextFunc
    self.addressFunc = addressFunc

  def address_bid(self, s: pd.Series) -> str:
    address = self.addressFunc(s)

    # encode for the model
    features = self.encodeTextFunc(address)

    # the length of the encoded text
    lengths = tf.constant([features[0]], dtype=tf.int64)

    # the encoded text
    encoded_texts = tf.constant([features[1]], dtype=tf.int64)

    # Call the serving function with the encoded texts and lengths
    predictions = self.servingDefault(
        encoded_text=encoded_texts,
        lengths=lengths,
    )

    # highest probability first
    for address, class_ids, probabilities in zip([address], predictions['class_ids'], predictions['probabilities']):
        mappings = self.map2Func(address, class_ids, probabilities)
        # TODO: validate probability and reject anything lower than a threshold - capture somehow so we can 
        # train or figure out some kind of mapping fallback
        result = []
        keys = ['property_name', 'street_address', 'postcode']
        if 'flat_number' in mappings:
           result.append(f"Flat {mappings['flat_number']['text']}")
        if 'unit_number' in mappings:
           result.append(f"Flat {mappings['unit_number']['text']}")
        if 'suite_number' in mappings:
           result.append(f"Flat {mappings['suite_number']['text']}")
        for key in keys:
          if key in mappings:
            result.append(mappings[key]['text'])
        result = '|'.join(result).replace(' ', '').upper()
        return result
