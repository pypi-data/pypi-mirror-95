import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IRenderMimeRegistry } from '@jupyterlab/rendermime';

import { requestAPI } from './handler';
import { WidgetRenderer } from './WidgetRenderer';

/**
 * The mime type for a widget view.
 */
export const WIDGET_VIEW_MIMETYPE = 'application/vnd.simlin.widget-view+json';

/**
 * Initialization data for the jupyter-simlin extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-simlin:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd, rendermime: IRenderMimeRegistry) => {
    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `:ohno: jupyter-simlin server extension appears to be missing.\n${reason}`
        );
      });

    rendermime.addFactory(
      {
        safe: false,
        mimeTypes: [WIDGET_VIEW_MIMETYPE],
        createRenderer: options => new WidgetRenderer(options)
      },
      0
    );
  },
  requires: [IRenderMimeRegistry],
};

export default extension;
