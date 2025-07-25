import React, { useState } from 'react';
import { ChevronDown, ChevronRight, FileText, Folder, Code, List, CheckCircle, AlertCircle } from 'lucide-react';

// Helper function to safely render content (handles both strings and objects)
const SafeContent = ({ content }) => {
  if (typeof content === 'string') {
    return content;
  } else if (typeof content === 'object' && content !== null) {
    // Handle object content by rendering key-value pairs
    return (
      <div className="space-y-1">
        {Object.entries(content).map(([key, value], index) => (
          <div key={index} className="text-sm">
            <span className="font-medium capitalize">{key.replace(/_/g, ' ')}:</span>{' '}
            <span>{typeof value === 'string' ? value : JSON.stringify(value)}</span>
          </div>
        ))}
      </div>
    );
  } else {
    return String(content);
  }
};

const PlanDisplay = ({ plan }) => {
  const [expandedSections, setExpandedSections] = useState({
    overview: true,
    technical: false,
    structure: false,
    files: false,
    implementation: false
  });

  console.log('🎨 PlanDisplay received plan:', plan);
  console.log('📊 Plan keys:', Object.keys(plan || {}));

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const renderSection = (title, icon, content, sectionKey) => {
    const isExpanded = expandedSections[sectionKey];
    
    return (
      <div className="bg-white rounded-lg shadow-md mb-4 overflow-hidden">
        <button
          onClick={() => toggleSection(sectionKey)}
          className="w-full px-6 py-4 flex items-center justify-between bg-gray-50 hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center">
            {icon}
            <h3 className="text-lg font-semibold text-gray-900 ml-3">{title}</h3>
          </div>
          {isExpanded ? (
            <ChevronDown className="h-5 w-5 text-gray-500" />
          ) : (
            <ChevronRight className="h-5 w-5 text-gray-500" />
          )}
        </button>
        
        {isExpanded && (
          <div className="px-6 py-4">
            {content}
          </div>
        )}
      </div>
    );
  };

  const renderProjectOverview = () => {
    // Handle different structures for project overview
    const overview = plan.project_overview || {};
    const name = plan.project_name || overview.name || overview.project_name;
    const description = plan.project_description || overview.description || overview.project_description;
    const purpose = overview.purpose || overview.main_functionality;
    const audience = plan.target_audience || overview.target_audience;
    
    return (
      <div className="space-y-4">
        {name && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Project Name</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={name} />
            </div>
          </div>
        )}
        
        {description && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Description</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={description} />
            </div>
          </div>
        )}
        
        {purpose && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Purpose</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={purpose} />
            </div>
          </div>
        )}
        
        {audience && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Target Audience</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={audience} />
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderTechnicalRequirements = () => {
    const tech = plan.technical_requirements || {};
    return (
      <div className="space-y-4">
        {tech.python_version && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Python Version</h4>
            <p className="text-gray-700 bg-blue-50 p-3 rounded border border-blue-200">
              <SafeContent content={tech.python_version} />
            </p>
          </div>
        )}
        
        {tech.dependencies && Array.isArray(tech.dependencies) && tech.dependencies.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Required Libraries</h4>
            <div className="bg-gray-50 p-3 rounded">
              <ul className="space-y-1">
                {tech.dependencies.map((dep, index) => (
                  <li key={index} className="flex items-center text-gray-700">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                    <code className="text-sm bg-gray-200 px-2 py-1 rounded">{dep}</code>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
        
        {tech.gui_framework && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">GUI Framework</h4>
            <div className="bg-green-50 p-3 rounded border border-green-200">
              <p className="text-gray-700">
                <strong>{tech.gui_framework}</strong>
                {tech.gui_framework_justification && (
                  <span className="block mt-1 text-sm text-gray-600">
                    <SafeContent content={tech.gui_framework_justification} />
                  </span>
                )}
              </p>
            </div>
          </div>
        )}
        
        {tech.database_requirements && tech.database_requirements !== 'None' && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Database</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={tech.database_requirements} />
            </div>
          </div>
        )}
        
        {tech.external_apis && tech.external_apis !== 'None' && Array.isArray(tech.external_apis) && tech.external_apis.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">External APIs</h4>
            <ul className="bg-gray-50 p-3 rounded space-y-1">
              {tech.external_apis.map((api, index) => (
                <li key={index} className="text-gray-700">{api}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderProjectStructure = () => {
    const structure = plan.project_structure || {};
    return (
      <div className="space-y-4">
        {structure.root_directory && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Root Directory</h4>
            <p className="text-gray-700 bg-blue-50 p-3 rounded border border-blue-200">
              {structure.root_directory}
            </p>
          </div>
        )}
        
        {structure.directories && Array.isArray(structure.directories) && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Directories</h4>
            <div className="bg-gray-50 p-3 rounded space-y-2">
              {structure.directories.map((dir, index) => (
                <div key={index} className="flex items-start">
                  <Folder className="h-4 w-4 text-yellow-500 mr-2 mt-1" />
                  <div>
                    <code className="font-medium text-gray-900">{dir.name}</code>
                    {dir.purpose && (
                      <p className="text-sm text-gray-600 mt-1">{dir.purpose}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {structure.files && Array.isArray(structure.files) && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Key Files</h4>
            <div className="bg-gray-50 p-3 rounded space-y-2">
              {structure.files.map((file, index) => (
                <div key={index} className="flex items-start">
                  <FileText className="h-4 w-4 text-blue-500 mr-2 mt-1" />
                  <div>
                    <code className="font-medium text-gray-900">{file.path}</code>
                    {file.entry_point && (
                      <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                        Entry Point
                      </span>
                    )}
                    {file.purpose && (
                      <p className="text-sm text-gray-600 mt-1">{file.purpose}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {structure.folders && typeof structure.folders === 'string' && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Folder Structure</h4>
            <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm overflow-x-auto">
              <pre>{structure.folders}</pre>
            </div>
          </div>
        )}
        
        {structure.description && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Structure Description</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{structure.description}</p>
          </div>
        )}
      </div>
    );
  };

  const renderFileBreakdown = () => {
    const files = plan.file_breakdown || '';
    
    // Handle the new string format for file_breakdown
    if (typeof files === 'string') {
      return (
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-3">Project Files</h4>
            <div className="text-gray-700 whitespace-pre-line">
              <SafeContent content={files} />
            </div>
          </div>
        </div>
      );
    }
    
    // Fallback: Handle legacy object/array formats if they still exist
    let fileList = [];
    if (Array.isArray(files)) {
      fileList = files;
    } else if (files.files && Array.isArray(files.files)) {
      fileList = files.files;
    } else if (typeof files === 'object') {
      // Convert object to array format
      fileList = Object.entries(files).map(([filePath, fileInfo]) => {
        if (typeof fileInfo === 'object') {
          return {
            file_path: filePath,
            ...fileInfo
          };
        } else {
          return {
            file_path: filePath,
            purpose: fileInfo
          };
        }
      });
    }
    
    return (
      <div className="space-y-4">
        {fileList.map((fileInfo, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <FileText className="h-4 w-4 text-blue-500 mr-2" />
              <code className="font-medium text-gray-900 bg-gray-100 px-2 py-1 rounded">
                {fileInfo.file_path || fileInfo.path || `File ${index + 1}`}
              </code>
            </div>
            
            <div className="space-y-2 ml-6">
              {fileInfo.purpose && (
                <p className="text-gray-700"><strong>Purpose:</strong> <SafeContent content={fileInfo.purpose} /></p>
              )}
              {fileInfo.functionality && (
                <p className="text-gray-700"><strong>Functionality:</strong> <SafeContent content={fileInfo.functionality} /></p>
              )}
              {fileInfo.components && Array.isArray(fileInfo.components) && fileInfo.components.length > 0 && (
                <div>
                  <strong className="text-gray-700">Key Components:</strong>
                  <ul className="list-disc list-inside ml-4 text-gray-600">
                    {fileInfo.components.map((component, idx) => (
                      <li key={idx}>{component}</li>
                    ))}
                  </ul>
                </div>
              )}
              {fileInfo.dependencies && (
                <div>
                  <strong className="text-gray-700">Dependencies:</strong>
                  {Array.isArray(fileInfo.dependencies) ? (
                    <ul className="list-disc list-inside ml-4 text-gray-600">
                      {fileInfo.dependencies.map((dep, idx) => (
                        <li key={idx}><code className="text-sm bg-gray-100 px-1 rounded">{dep}</code></li>
                      ))}
                    </ul>
                  ) : (
                    <span className="ml-2 text-gray-600">{fileInfo.dependencies}</span>
                  )}
                </div>
              )}
              {fileInfo.interactions && (
                <p className="text-gray-700"><strong>Interactions:</strong> <SafeContent content={fileInfo.interactions} /></p>
              )}
            </div>
          </div>
        ))}
        
        {fileList.length === 0 && (
          <p className="text-gray-500 italic">No file breakdown available</p>
        )}
      </div>
    );
  };

  const renderImplementationStrategy = () => {
    const impl = plan.implementation_strategy || {};
    return (
      <div className="space-y-4">
        {impl.phases && Array.isArray(impl.phases) && impl.phases.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Development Phases</h4>
            <ol className="space-y-2">
              {impl.phases.map((phase, index) => (
                <li key={index} className="flex items-start bg-gray-50 p-3 rounded">
                  <span className="bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm mr-3 mt-0.5">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{phase}</span>
                </li>
              ))}
            </ol>
          </div>
        )}
        
        {impl.development_phases && Array.isArray(impl.development_phases) && impl.development_phases.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Development Phases</h4>
            <ol className="space-y-2">
              {impl.development_phases.map((phase, index) => (
                <li key={index} className="flex items-start bg-gray-50 p-3 rounded">
                  <span className="bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm mr-3 mt-0.5">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{phase}</span>
                </li>
              ))}
            </ol>
          </div>
        )}
        
        {impl.development_phases && typeof impl.development_phases === 'string' && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Development Phases</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={impl.development_phases} />
            </div>
          </div>
        )}
        
        {impl.test_file_requirements && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Test File Requirements</h4>
            <div className="text-gray-700 bg-gray-50 p-3 rounded">
              <SafeContent content={impl.test_file_requirements} />
            </div>
          </div>
        )}
        
        {impl.deployment_considerations && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Deployment Considerations</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{impl.deployment_considerations}</p>
          </div>
        )}
        
        {impl.critical_components && Array.isArray(impl.critical_components) && impl.critical_components.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Critical Components</h4>
            <ul className="space-y-1">
              {impl.critical_components.map((component, index) => (
                <li key={index} className="flex items-center text-gray-700">
                  <AlertCircle className="h-4 w-4 text-orange-500 mr-2" />
                  {component}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {impl.testing_strategy && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Testing Strategy</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{impl.testing_strategy}</p>
          </div>
        )}
        
        {impl.deployment && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Deployment</h4>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">{impl.deployment}</p>
          </div>
        )}
      </div>
    );
  };

  // Handle raw text plans (fallback)
  if (plan.format === 'text' || typeof plan === 'string') {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <FileText className="h-6 w-6 text-indigo-600 mr-2" />
          Generated Project Plan
        </h2>
        <div className="bg-gray-50 p-4 rounded-lg">
          <pre className="whitespace-pre-wrap text-gray-700 text-sm">
            {plan.raw_plan || plan}
          </pre>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center">
          <Code className="h-8 w-8 text-indigo-600 mr-3" />
          Generated Project Plan
        </h2>
        <p className="text-gray-600">
          Your AI-generated Python project plan is ready. Expand sections to see details.
        </p>
      </div>

      {renderSection(
        "Project Overview",
        <FileText className="h-5 w-5 text-blue-500" />,
        renderProjectOverview(),
        "overview"
      )}

      {renderSection(
        "Technical Requirements",
        <Code className="h-5 w-5 text-green-500" />,
        renderTechnicalRequirements(),
        "technical"
      )}

      {renderSection(
        "Project Structure",
        <Folder className="h-5 w-5 text-yellow-500" />,
        renderProjectStructure(),
        "structure"
      )}

      {renderSection(
        "File Breakdown",
        <List className="h-5 w-5 text-purple-500" />,
        renderFileBreakdown(),
        "files"
      )}

      {renderSection(
        "Implementation Strategy",
        <CheckCircle className="h-5 w-5 text-indigo-500" />,
        renderImplementationStrategy(),
        "implementation"
      )}
    </div>
  );
};

export default PlanDisplay;
