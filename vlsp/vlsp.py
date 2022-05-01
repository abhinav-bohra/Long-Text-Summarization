"""vlsp dataset."""
import json
import os

import tensorflow as tf
import tensorflow_datasets.public_api as tfds


_DESCRIPTION = """
Scientific papers datasets contains two sets of long and structured documents.

  - input: the body of the document, pagragraphs seperated by "/n".
  - output: the abstract of the document, pagragraphs seperated by "/n".

"""

_DOCUMENT = "input"
_SUMMARY = "output"

class VlspConfig(tfds.core.BuilderConfig):
  """BuilderConfig for Scientific Papers."""

  def __init__(self, *, filename=None, **kwargs):
    """BuilderConfig for Wikihow.

    Args:
      filename: filename of different configs for the dataset.
      **kwargs: keyword arguments forwarded to super.
    """
    # 1.1.0 remove sentence breaker <S> and </S> in summary.
    super(VlspConfig, self).__init__(
        version=tfds.core.Version("1.1.1"),
        supported_versions=[tfds.core.Version("1.1.0")],
        **kwargs)  # pytype: disable=wrong-arg-types  # gen-stub-imports
    self.filename = filename
    self.dl_manager = None



class Vlsp(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for vlsp dataset."""

  BUILDER_CONFIGS = [
      VlspConfig(name="vlsp", description="Scientific Papers.")
  ]

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""

    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            _DOCUMENT: tfds.features.Text(),
            _SUMMARY: tfds.features.Text(),
        }),
        supervised_keys=(_DOCUMENT, _SUMMARY),
        homepage=None,
        citation=None,
    )


  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(vlsp): Downloads the data and defines the splits
    # dl_manager is a tfds.download.DownloadManager that can be used to download and extract URLs
    # dl_paths = dl_manager.download_and_extract(_URLS)
    path = os.path.join("vlsp")
    print(f"Path: {path}")

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"path": os.path.join("train.json")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={"path": os.path.join("val.json")},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={"path": os.path.join("test.json")},
        ),
    ]


  def _generate_examples(self, path=None):
    """Yields examples."""
    # TODO(vlsp): Yields (key, example) tuples from the dataset
    with tf.io.gfile.GFile(path) as f:
      article_count = 0
      for line in f:
        # Possible keys are:
        # "article_id": str
        # "_DOCUMENT": list[str] article (list of paragraphs).
        # "_SUMMARY": list[str], abstract (list of paragraphs).
        
        # In original paper, <S> and </S> are not used in vocab during training or during decoding.
        # https://github.com/armancohan/long-summarization/blob/master/data.py#L27
        
        d = json.loads(line)
        summary = "\n".join(d[_SUMMARY])
        summary = summary.replace("<S>", "").replace("</S>", "")
        article_count = article_count + 1
        yield article_count, {
            _DOCUMENT: "\n".join(d[_DOCUMENT]),
            _SUMMARY: summary
        }
