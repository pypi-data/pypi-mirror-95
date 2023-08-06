import { datamodel } from '@system-dynamics/core';
import { renderSvgToString } from '@system-dynamics/diagram';
import { fromXmile } from '@system-dynamics/importer';
import { convertMdlToXmile } from '@system-dynamics/xmutil';

import { fromBase64 } from 'js-base64';

import { IDisposable } from '@lumino/disposable';

import { Panel } from '@lumino/widgets';

import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

export class WidgetRenderer
  extends Panel
  implements IRenderMime.IRenderer, IDisposable {
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this.mimeType = options.mimeType;
  }

  async renderModel(mimeModel: IRenderMime.IMimeModel): Promise<void> {
    const source: any = mimeModel.data[this.mimeType];

    const projectId: string = source['project_id'];
    let contents = source['project_source'];
    let project: datamodel.Project;
    if (projectId.endsWith('.mdl')) {
      contents = await convertMdlToXmile(fromBase64(contents), false);
      const pb = await fromXmile(contents);
      project = datamodel.Project.deserializeBinary(pb);
    } else if (projectId.endsWith('.stmx') || projectId.endsWith('.xmile')) {
      const pb = await fromXmile(fromBase64(contents));
      project = datamodel.Project.deserializeBinary(pb);
    } else {
      project = datamodel.Project.deserializeBase64(contents);
    }

    const [svg] = await renderSvgToString(project, 'main');

    // Let's be optimistic, and hope the widget state will come later.
    console.log('woooomp');
    this.node.innerHTML = svg;

    // If there is no model id, the view was removed, so hide the node.
    if (source.model_id === '') {
      this.hide();
      return;
    }
  }

  dispose(): void {
    super.dispose();
    // TODO: finalize react-y stuff?
  }

  /**
   * The mimetype being rendered.
   */
  readonly mimeType: string;
}
