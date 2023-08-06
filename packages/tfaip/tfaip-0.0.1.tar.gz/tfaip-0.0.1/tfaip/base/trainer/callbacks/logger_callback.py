# Copyright 2020 The tfaip authors. All Rights Reserved.
#
# This file is part of tfaip.
#
# tfaip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# tfaip is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# tfaip. If not, see http://www.gnu.org/licenses/.
# ==============================================================================
from tensorflow.keras.callbacks import Callback
import logging


logger = logging.getLogger(__name__)


class LoggerCallback(Callback):
    def on_epoch_begin(self, epoch, logs=None):
        logger.info(f"Start of epoch {epoch + 1:4d}")

    def on_epoch_end(self, epoch, logs=None):
        if logs is None:
            return
        logs_str = ' - '.join(f"{k}: {logs[k]:.4f}" for k in sorted(logs.keys()))
        logger.info(f"Results of epoch {epoch + 1:4d}: {logs_str}")
