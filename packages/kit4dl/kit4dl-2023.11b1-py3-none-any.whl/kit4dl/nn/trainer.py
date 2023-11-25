"""A module with neural network train task definition."""

import os
import logging
from typing import Any

import lightning.pytorch as pl
from lightning.pytorch import callbacks as pl_callbacks
from lightning.pytorch import loggers as pl_log

from kit4dl.dataset import Kit4DLAbstractDataModule
from kit4dl.mixins import LoggerMixin
from kit4dl.nn.base import Kit4DLAbstractModule
from kit4dl.nn.callbacks import MetricCallback
from kit4dl.nn.confmodels import Conf
from kit4dl.utils import set_seed
from kit4dl import io as io_


class Trainer(LoggerMixin):
    """Class managing the training procedure."""

    _model: Kit4DLAbstractModule
    _datamodule: Kit4DLAbstractDataModule
    _pl_trainer: pl.Trainer
    _conf: Conf
    _metric_logger: Any

    def __init__(self, conf: Conf) -> None:
        self._logger = logging.getLogger("lightning.pytorch")
        self._conf = conf
        self._device = self._conf.base.device
        self._metric_logger = self._new_metric_logger()
        set_seed(self._conf.base.seed)

    @property
    def is_finished(self) -> bool:
        """Check if training routing finished."""
        return self._pl_trainer.state.finished

    def prepare(self) -> "Trainer":
        """Prepare trainer by configuring the model and data modules."""
        self._model = self._configure_model()
        self._pl_trainer = self._configure_trainer()
        self._datamodule = self._configure_datamodule()
        self._log_hparams()
        return self

    def _log_hparams(self) -> None:
        self._metric_logger.log_hyperparams(self._conf.dict())
        self._metric_logger.log_hyperparams(
            {
                "trainable_parameters": sum(
                    p.numel()
                    for p in self._model.parameters()
                    if p.requires_grad
                )
            }
        )

    def load_checkpoint(self, path: str) -> Kit4DLAbstractModule:
        """Load model weights from the checkpoint."""
        model = type(self._model).load_from_checkpoint(path)
        model.freeze()
        return model

    def fit(self) -> "Trainer":
        """Fit the trainer making use of `lightning.pytorch.Trainer`."""
        assert self._pl_trainer, (
            "trainer is not configured. did you forget to call `prepare()`"
            " method first?"
        )
        self._pl_trainer.fit(self._model, datamodule=self._datamodule)
        return self

    def test(self) -> "Trainer":
        """Test the model."""
        assert self._pl_trainer, (
            "trainer is not configured. did you forget to call `prepare()`"
            " method first?"
        )
        ckpt_path = None
        for callback in self._pl_trainer.checkpoint_callbacks:
            if isinstance(callback, pl_callbacks.ModelCheckpoint):
                self.debug(
                    "best checkpoint taken from callback %s",
                    callback.best_model_path,
                )
                ckpt_path = callback.best_model_path
                break
        if self._conf.training.checkpoint_path:
            assert os.path.exists(self._conf.training.checkpoint_path), (
                "the defined checkpoint:"
                f" {self._conf.training.checkpoint_path} does not exist!"
            )
            self.info(
                "user-defined checkpoint %s will be used for testing",
                self._conf.training.checkpoint_path,
            )
            ckpt_path = self._conf.training.checkpoint_path
        if ckpt_path:
            self._model = self.load_checkpoint(ckpt_path)
        self._pl_trainer.test(
            self._model, datamodule=self._datamodule, ckpt_path=ckpt_path
        )
        return self

    def predict(self) -> "Trainer":
        """Predict values for the model."""
        assert self._pl_trainer, (
            "trainer is not configured. did you forget to call `prepare()`"
            " method first?"
        )
        self._pl_trainer.predict(self._model, datamodule=self._datamodule)
        return self

    def _new_metric_logger(self) -> pl_log.Logger:
        return self._conf.logging.metric_logger_type(
            **self._conf.logging.arguments
        )

    def _configure_datamodule(self) -> Kit4DLAbstractDataModule:
        class_ = self._conf.dataset.datamodule_class
        io_.assert_valid_class(class_, Kit4DLAbstractDataModule)
        return self._conf.dataset.datamodule_class(conf=self._conf.dataset)

    def _configure_model(self) -> Kit4DLAbstractModule:
        class_ = self._conf.model.model_class
        io_.assert_valid_class(class_, Kit4DLAbstractModule)
        return self._conf.model.model_class(conf=self._conf).to(self._device)

    def _get_model_checkpoint(self) -> pl_callbacks.ModelCheckpoint:
        assert self._conf.training.checkpoint, (
            "getting model checkpoint callback, but `checkpoint` was not"
            " defined in the configuration file"
        )
        chkp_conf = self._conf.training.checkpoint
        assert (not chkp_conf.every_n_epochs) or isinstance(
            chkp_conf.every_n_epochs, int
        ), (
            "wrong type of `every_n_epochs`. expected: `int`, provided:"
            f" {type(chkp_conf.every_n_epochs)}"
        )
        return pl_callbacks.ModelCheckpoint(
            dirpath=chkp_conf.path,
            filename=chkp_conf.filename,
            monitor=chkp_conf.monitor_metric_name,
            save_top_k=chkp_conf.save_top_k,
            mode=chkp_conf.mode,
            save_weights_only=chkp_conf.save_weights_only,
            every_n_epochs=chkp_conf.every_n_epochs,
            save_on_train_epoch_end=chkp_conf.save_on_train_epoch_end,
        )

    def _set_default_trainer_args(self):
        self._conf.training.arguments.setdefault("deterministic", True)
        self._conf.training.arguments.setdefault("enable_progress_bar", True)

    def _configure_trainer(self) -> pl.Trainer:
        accelerator_device, device = self._conf.base.accelerator_device_and_id
        callbacks: list[pl_callbacks.Callback] = [
            MetricCallback(conf=self._conf.metrics_obj)
        ] + self._conf.training.preconfigured_callbacks
        if self._conf.training.checkpoint:
            callbacks.append(self._get_model_checkpoint())
        return pl.Trainer(
            accelerator=accelerator_device,
            devices=device,
            max_epochs=self._conf.training.epochs,
            check_val_every_n_epoch=self._conf.validation.run_every_epoch,
            logger=self._metric_logger,
            callbacks=callbacks,
            **self._conf.training.arguments,
        )
