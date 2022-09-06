import kfp
import kfp.components as comp
from kubernetes.client.models import V1EnvVar

@kfp.dsl.component
def get_data():
    # Defining component configuration
    getdata_component = kfp.dsl.ContainerOp(
        name='Data-Preparation',
        image='docker.io/depankars/kubeflow-sdk-farmer',
        command=['python', 'get_data.py'],
        )
    return getdata_component
  
@kfp.dsl.component
def data_preprocessing():    
    # Defining component configuration
    data_preprocessing = kfp.dsl.ContainerOp(
        name='data-preprocessing',
        image='docker.io/depankars/kubeflow-sdk-farmer',
        command=['python', 'process_data.py'],
        )
    return data_preprocessing
  
@kfp.dsl.component
def training():
    # Defining component configuration
    training_component = kfp.dsl.ContainerOp(
        name='training',
        image='docker.io/depankars/kubeflow-sdk-farmer',
        command=['python', 'train.py'],
        file_outputs={'mlpipeline-ui-metadata':'/mlpipeline-ui-metadata.json', "mlpipeline-metrics":'/mlpipeline-metrics.json'}
        )
    
    return training_component
# Let see output of component configuration
debug = True
if debug :
    training_component_vis = training()
    print(training_component_vis)
    
@kfp.dsl.pipeline(
  name="Modeling Swiss farmer's attitudes about",
  description="Modeling Swiss farmer's attitudes about"
)
def farmer():
    download_data = get_data()
    download_data.execution_options.caching_strategy.max_cache_staleness = "P0D"
    data_processing = data_preprocessing().after(download_data)
    data_processing.execution_options.caching_strategy.max_cache_staleness = "P0D"
    train = training().after(data_processing)
    train.execution_options.caching_strategy.max_cache_staleness = "P0D"    
# Let see output of pipeline configuration
debug = True
if debug :
    training_pipeline_output = farmer()
    print(training_pipeline_output)    
