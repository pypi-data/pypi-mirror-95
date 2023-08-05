import tensorflow.keras.callbacks as clb


def get_default_callbacks(model_path, monitor='val_acc', verbose=1):
    return [
        clb.ReduceLROnPlateau(monitor=monitor, factor=0.5, min_lr=1e-7, patience=3, verbose=verbose),
        clb.EarlyStopping(monitor=monitor, patience=7, verbose=verbose),
        clb.ModelCheckpoint(monitor=monitor, filepath=model_path, save_best_only=True, verbose=verbose)
    ]
