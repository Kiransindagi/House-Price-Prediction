import React, { useState, useEffect } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('Valuation');
  const [systemInfo, setSystemInfo] = useState({ status: 'unknown', model_version: 'unknown' });
  const [modelInfo, setModelInfo] = useState(null);
  
  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then(res => res.json())
      .then(data => setSystemInfo(data))
      .catch(err => console.error(err));
      
    fetch(`${API_BASE_URL}/model-info`)
      .then(res => res.json())
      .then(data => setModelInfo(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="app-container">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="main-content">
        <TopHeader 
          activeTab={activeTab} 
          status={systemInfo.status} 
          modelName={modelInfo?.model_name || 'Loading...'} 
          version={systemInfo.model_version} 
        />
        
        <div className="page-content">
          {activeTab === 'Valuation' && <ValuationPage />}
          {activeTab === 'Property Analysis' && <PropertyAnalysisPage />}
          {activeTab === 'Model Insights' && <ModelInsightsPage apiBase={API_BASE_URL} />}
          {activeTab === 'Performance' && <PerformancePage />}
          {activeTab === 'System Information' && <SystemInfoPage systemInfo={systemInfo} modelInfo={modelInfo} />}
        </div>
      </div>
    </div>
  );
}

function Sidebar({ activeTab, setActiveTab }) {
  const tabs = ['Valuation', 'Property Analysis', 'Model Insights', 'Performance', 'System Information'];
  return (
    <div className="sidebar">
      <h1>House Price AI</h1>
      <div className="nav-links">
        {tabs.map(tab => (
          <div 
            key={tab} 
            className={`nav-link ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </div>
        ))}
      </div>
    </div>
  );
}

function TopHeader({ activeTab, status, modelName, version }) {
  const isConnected = status === 'ok';
  return (
    <div className="top-header">
      <h2>{activeTab}</h2>
      <div className="status-indicator">
        <span>{modelName} (v{version})</span>
        <div className={`status-dot ${isConnected ? 'connected' : ''}`}></div>
        <span>{isConnected ? 'API Connected' : 'Disconnected'}</span>
      </div>
    </div>
  );
}

function ValuationPage() {
  const [formData, setFormData] = useState({
    LotArea: 8450, GrLivArea: 1710, TotalBsmtSF: 856, GarageArea: 548,
    OverallQual: 7, OverallCond: 5, YearBuilt: 2003, YearRemodAdd: 2003,
    BedroomAbvGr: 3, FullBath: 2, HalfBath: 1, TotRmsAbvGrd: 8,
    Neighborhood: 'CollgCr', MSZoning: 'RL', FireplaceQu: 'NA',
    PoolArea: 0, Fence: 'NA', SaleType: 'WD', SaleCondition: 'Normal'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (res.ok) {
        setResult(data);
      } else {
        setError(data.detail || 'Prediction failed');
      }
    } catch (err) {
      setError('Network error: API unavailable');
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="card">
        <h2>Property Valuation</h2>
        <form onSubmit={handleSubmit}>
          
          <h3 style={{marginTop: '1rem', marginBottom: '0.5rem'}}>Property Size</h3>
          <div className="form-grid">
            <div className="form-group"><label>Lot Area (sqft)</label><input type="number" className="form-control" name="LotArea" value={formData.LotArea} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Living Area (sqft)</label><input type="number" className="form-control" name="GrLivArea" value={formData.GrLivArea} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Basement Area (sqft)</label><input type="number" className="form-control" name="TotalBsmtSF" value={formData.TotalBsmtSF} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Garage Area (sqft)</label><input type="number" className="form-control" name="GarageArea" value={formData.GarageArea} onChange={handleChange} required min="0"/></div>
          </div>

          <h3 style={{marginTop: '1rem', marginBottom: '0.5rem'}}>Quality and Age</h3>
          <div className="form-grid">
            <div className="form-group"><label>Overall Quality (1-10)</label><input type="number" className="form-control" name="OverallQual" value={formData.OverallQual} onChange={handleChange} required min="1" max="10"/></div>
            <div className="form-group"><label>Overall Condition (1-10)</label><input type="number" className="form-control" name="OverallCond" value={formData.OverallCond} onChange={handleChange} required min="1" max="10"/></div>
            <div className="form-group"><label>Year Built</label><input type="number" className="form-control" name="YearBuilt" value={formData.YearBuilt} onChange={handleChange} required min="1800"/></div>
            <div className="form-group"><label>Year Remodeled</label><input type="number" className="form-control" name="YearRemodAdd" value={formData.YearRemodAdd} onChange={handleChange} required min="1800"/></div>
          </div>

          <h3 style={{marginTop: '1rem', marginBottom: '0.5rem'}}>Rooms</h3>
          <div className="form-grid">
            <div className="form-group"><label>Bedrooms</label><input type="number" className="form-control" name="BedroomAbvGr" value={formData.BedroomAbvGr} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Full Baths</label><input type="number" className="form-control" name="FullBath" value={formData.FullBath} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Half Baths</label><input type="number" className="form-control" name="HalfBath" value={formData.HalfBath} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Total Rooms</label><input type="number" className="form-control" name="TotRmsAbvGrd" value={formData.TotRmsAbvGrd} onChange={handleChange} required min="0"/></div>
          </div>

          <h3 style={{marginTop: '1rem', marginBottom: '0.5rem'}}>Location & Extras</h3>
          <div className="form-grid">
            <div className="form-group"><label>Neighborhood</label>
              <select className="form-control" name="Neighborhood" value={formData.Neighborhood} onChange={handleChange}>
                <option value="CollgCr">College Creek</option>
                <option value="Veenker">Veenker</option>
                <option value="Crawfor">Crawford</option>
                <option value="NoRidge">Northridge</option>
                <option value="Mitchel">Mitchell</option>
                <option value="NAmes">North Ames</option>
                <option value="OldTown">Old Town</option>
              </select>
            </div>
            <div className="form-group"><label>Zoning</label>
              <select className="form-control" name="MSZoning" value={formData.MSZoning} onChange={handleChange}>
                <option value="RL">Residential Low Density</option>
                <option value="RM">Residential Medium Density</option>
                <option value="FV">Floating Village Residential</option>
                <option value="RH">Residential High Density</option>
              </select>
            </div>
            <div className="form-group"><label>Pool Area (sqft)</label><input type="number" className="form-control" name="PoolArea" value={formData.PoolArea} onChange={handleChange} required min="0"/></div>
            <div className="form-group"><label>Sale Condition</label>
              <select className="form-control" name="SaleCondition" value={formData.SaleCondition} onChange={handleChange}>
                <option value="Normal">Normal</option>
                <option value="Abnorml">Abnormal</option>
                <option value="Partial">Partial</option>
              </select>
            </div>
          </div>

          <button type="submit" className="btn" style={{marginTop: '1.5rem'}} disabled={loading}>
            {loading ? 'Evaluating...' : 'Predict Sale Price'}
          </button>
        </form>
        
        {error && <div style={{color: '#ef4444', marginTop: '1rem'}}>{JSON.stringify(error)}</div>}
        
        {result && (
          <div className="result-box">
            <p>Estimated Sale Price</p>
            <div className="price-display">
              ${result.predicted_sale_price.toLocaleString(undefined, {maximumFractionDigits: 0})}
            </div>
            <p style={{fontSize: '0.875rem', color: 'var(--text-muted)'}}>
              Model: v{result.model_version} • Predicted at: {new Date(result.prediction_timestamp).toLocaleTimeString()}
            </p>
            
            <div style={{marginTop: '2rem', textAlign: 'left', backgroundColor: 'var(--bg-dark)', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--border)'}}>
              <h4 style={{marginBottom: '1rem', color: 'var(--text-main)'}}>Key Factors Influencing This Estimate</h4>
              <p style={{fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1.5rem'}}>
                The bars below represent the feature's contribution direction and relative magnitude in the Ridge model's transformed log-prediction space. They do not represent exact dollar amounts.
              </p>
              
              <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '2rem'}}>
                {result.top_positive_contributors?.map((c, i) => (
                  <div key={`pos-${i}`} style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                    <span style={{width: '150px', fontSize: '0.875rem', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}} title={c.feature}>{c.feature}</span>
                    <div style={{flex: 1, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', height: '12px'}}>
                      <div style={{width: `${Math.min(c.contribution * 100, 100)}%`, backgroundColor: '#10b981', height: '100%', borderRadius: '4px'}}></div>
                    </div>
                    <span style={{width: '60px', fontSize: '0.85rem', color: '#10b981', textAlign: 'right'}}>+{c.contribution.toFixed(3)}</span>
                  </div>
                ))}
                
                {result.top_negative_contributors?.map((c, i) => (
                  <div key={`neg-${i}`} style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                    <span style={{width: '150px', fontSize: '0.875rem', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}} title={c.feature}>{c.feature}</span>
                    <div style={{flex: 1, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', height: '12px', display: 'flex', justifyContent: 'flex-end'}}>
                      <div style={{width: `${Math.min(Math.abs(c.contribution) * 100, 100)}%`, backgroundColor: '#ef4444', height: '100%', borderRadius: '4px'}}></div>
                    </div>
                    <span style={{width: '60px', fontSize: '0.85rem', color: '#ef4444', textAlign: 'right'}}>{c.contribution.toFixed(3)}</span>
                  </div>
                ))}
              </div>

              <div style={{backgroundColor: '#1e293b', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1.5rem'}}>
                <h4 style={{marginBottom: '0.75rem', color: 'var(--text-main)'}}>Property Profile Summary (Descriptive)</h4>
                <ul style={{fontSize: '0.875rem', color: 'var(--text-muted)', paddingLeft: '1.2rem', lineHeight: '1.6'}}>
                  {formData.YearBuilt >= 2010 && <li>Modern construction (Built in {formData.YearBuilt})</li>}
                  {formData.YearBuilt < 2010 && <li>Older construction (Built in {formData.YearBuilt})</li>}
                  {formData.YearRemodAdd >= 2015 && <li>Recently remodeled</li>}
                  {formData.GrLivArea > 2000 && <li>Large living area ({formData.GrLivArea} sqft)</li>}
                  {formData.OverallQual >= 8 && <li>High overall quality rating</li>}
                  {formData.PoolArea > 0 && <li>Pool present</li>}
                </ul>
              </div>

              <div style={{backgroundColor: '#1e293b', padding: '1rem', borderRadius: '0.5rem', fontFamily: 'monospace', fontSize: '0.85rem', color: '#a78bfa', overflowX: 'auto'}}>
                <div style={{color: 'var(--text-main)', marginBottom: '0.5rem', fontWeight: 'bold', fontFamily: 'sans-serif'}}>How the Ridge Model Produces an Estimate:</div>
                <div>Input Property &rarr; Missing Value Handling &rarr; Categorical Encoding &rarr; Numerical Scaling &rarr; Ridge Regression &rarr; Log-Space Prediction &rarr; expm1 Conversion &rarr; Estimated Sale Price</div>
                <br/>
                <div style={{color: '#94a3b8'}}>// Mathematical representation</div>
                <div>log(price) = intercept + &Sigma;(coefficient &times; transformed feature)</div>
                <div>price = expm1(log(price))</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function PropertyAnalysisPage() {
  return (
    <div className="card">
      <h2>Property Analysis</h2>
      <p>Derived analytics based on selected property parameters will appear here.</p>
    </div>
  );
}

function ModelInsightsPage({ apiBase }) {
  return (
    <div className="card">
      <h2>Model Insights</h2>
      
      <div style={{marginBottom: '2rem'}}>
        <h3>Feature Importance & SHAP Analysis</h3>
        <p style={{color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '0.5rem', marginBottom: '1rem'}}>
          The chart below explains how different features influence the model's predictions using SHapley Additive exPlanations (SHAP).
        </p>
        <div style={{ background: '#fff', padding: '1rem', borderRadius: '0.5rem', textAlign: 'center' }}>
          <img 
            src={`${apiBase}/figures/shap_summary.png`} 
            alt="SHAP Summary" 
            style={{ maxWidth: '100%', height: 'auto', borderRadius: '0.25rem' }} 
            onError={(e) => { e.target.style.display = 'none'; e.target.parentNode.innerHTML += '<p style="color: #000;">SHAP Graph not available.</p>' }}
          />
        </div>
      </div>

      <div style={{marginBottom: '2rem'}}>
        <h3>Target Transformation (Log1p)</h3>
        <div className="form-grid" style={{ marginTop: '1rem' }}>
          <div style={{ background: '#fff', padding: '0.5rem', borderRadius: '0.5rem', textAlign: 'center' }}>
            <h4 style={{color: '#334155'}}>Before (Skewness: 1.88)</h4>
            <img src={`${apiBase}/figures/target_distribution.png`} alt="Original Distribution" style={{ width: '100%', height: 'auto', borderRadius: '0.25rem' }} />
          </div>
          <div style={{ background: '#fff', padding: '0.5rem', borderRadius: '0.5rem', textAlign: 'center' }}>
            <h4 style={{color: '#334155'}}>After (Skewness: 0.12)</h4>
            <img src={`${apiBase}/figures/log_target_distribution.png`} alt="Log Transformed" style={{ width: '100%', height: 'auto', borderRadius: '0.25rem' }} />
          </div>
        </div>
        <p style={{color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '1rem'}}>
          Housing prices are commonly right-skewed. The Log transformation reduces the influence of extreme values (highly skewed real estate prices) improving residual behavior for linear models.
        </p>
      </div>
      
      <div style={{marginBottom: '1.5rem'}}>
        <h3>Multicollinearity Findings (VIF)</h3>
        <ul>
          <li><strong>GrLivArea VIF:</strong> ~41.80</li>
          <li><strong>TotRmsAbvGrd VIF:</strong> ~73.11</li>
        </ul>
        <p style={{color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '0.5rem'}}>
          High VIF implies strong correlation among features. While linear model coefficients can become unstable, Ridge regularization mitigates this issue by penalizing large weights.
        </p>
      </div>
    </div>
  );
}

function PerformancePage() {
  return (
    <div className="card">
      <h2>Model Performance</h2>
      <p style={{marginBottom: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)'}}>
        Metrics derived from holdout test set in the original price space.
      </p>
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>RMSE</th>
            <th>MAE</th>
            <th>R²</th>
          </tr>
        </thead>
        <tbody>
          <tr style={{backgroundColor: 'rgba(59, 130, 246, 0.1)'}}>
            <td><strong>Ridge (Champion)</strong></td>
            <td>$25,053.84</td>
            <td>$16,415.17</td>
            <td>0.9182</td>
          </tr>
          <tr>
            <td>Lasso</td>
            <td>$25,156.00</td>
            <td>$16,332.02</td>
            <td>0.9175</td>
          </tr>
          <tr>
            <td>Random Forest</td>
            <td>$28,750.83</td>
            <td>$17,581.10</td>
            <td>0.8922</td>
          </tr>
          <tr>
            <td>Gradient Boosting</td>
            <td>$28,950.07</td>
            <td>$16,794.65</td>
            <td>0.8907</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

function SystemInfoPage({ systemInfo, modelInfo }) {
  return (
    <div className="card">
      <h2>System Information</h2>
      <div className="form-grid">
        <div>
          <h4>API Status</h4>
          <p>{systemInfo.status}</p>
        </div>
        <div>
          <h4>Model Availability</h4>
          <p>{systemInfo.model_availability}</p>
        </div>
        <div>
          <h4>Champion Model</h4>
          <p>{modelInfo?.model_name || 'Loading...'}</p>
        </div>
        <div>
          <h4>Model Version</h4>
          <p>{modelInfo?.version || 'Loading...'}</p>
        </div>
      </div>
      
      <h3 style={{marginTop: '2rem'}}>Endpoints</h3>
      <ul style={{marginTop: '0.5rem', color: 'var(--text-muted)', paddingLeft: '1.5rem'}}>
        <li>GET /api/health</li>
        <li>GET /api/model-info</li>
        <li>POST /api/predict</li>
      </ul>
    </div>
  );
}

export default App;
