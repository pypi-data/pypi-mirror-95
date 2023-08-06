"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import datetime as dt
from typing import List, Dict

from gs_quant.api.gs.risk_models import GsRiskModelApi
from gs_quant.target.risk_models import RiskModelData, RiskModelCalendar, RiskModelFactor, \
    DataAssetsRequest, Measure, Format


class RiskModel:

    def __init__(self, model_id: str):
        self.model = GsRiskModelApi.get_risk_model(model_id)

    def get_id(self) -> str:
        """ Retrieve risk model id for existing risk model """
        return self.model.id

    def get_dates(self, start_date: dt.date = None, end_date: dt.date = None) -> List:
        """ Retrieve risk model dates for existing risk model """
        return GsRiskModelApi.get_risk_model_dates(self.model.id, start_date, end_date)

    def get_factor(self, factor_id: str) -> RiskModelFactor:
        """ Retrieve risk model factor from model and factor ids """
        return GsRiskModelApi.get_risk_model_factor(self.model.id, factor_id)

    def create_factor(self, factor: RiskModelFactor):
        """ Create a new risk model factor """
        GsRiskModelApi.create_risk_model_factor(self.model.id, factor)

    def update_factor(self, factor_id: str, factor: RiskModelFactor):
        """ Update existing risk model factor """
        GsRiskModelApi.update_risk_model_factor(self.model.id, factor_id, factor)

    def delete_factor(self, factor_id: str):
        """ Delete a risk model factor """
        GsRiskModelApi.delete_risk_model_factor(self.model.id, factor_id)

    def get_factor_data(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        identifiers: List[str] = None,
                        include_performance_curve: bool = None) -> List[Dict]:
        """ Retrieve factor data for existing risk model """
        return GsRiskModelApi.get_risk_model_factor_data(self.model.id,
                                                         start_date,
                                                         end_date,
                                                         identifiers,
                                                         include_performance_curve)

    def get_calendar(self) -> RiskModelCalendar:
        """ Retrieve risk model calendar for existing risk model """
        return GsRiskModelApi.get_risk_model_calendar(self.model.id)

    def upload_calendar(self, calendar: RiskModelCalendar):
        """ Upload risk model calendar to existing risk model """
        return GsRiskModelApi.upload_risk_model_calendar(self.model.id, calendar)

    def get_asset_universe(self,
                           start_date: dt.date,
                           end_date: dt.date,
                           assets: DataAssetsRequest = None,
                           data_format: Format = None) -> Dict:
        """ Retrieve asset universe data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_historical_beta(self,
                            start_date: dt.date,
                            end_date: dt.date,
                            assets: DataAssetsRequest = None,
                            data_format: Format = None) -> Dict:
        """ Retrieve historical beta data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Historical_Beta, Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_total_risk(self,
                       start_date: dt.date,
                       end_date: dt.date,
                       assets: DataAssetsRequest = None,
                       data_format: Format = None) -> Dict:
        """ Retrieve total risk data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Total_Risk, Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_specific_risk(self,
                          start_date: dt.date,
                          end_date: dt.date,
                          assets: DataAssetsRequest = None,
                          data_format: Format = None) -> Dict:
        """ Retrieve specific risk data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Specific_Risk, Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_residual_variance(self,
                              start_date: dt.date,
                              end_date: dt.date,
                              assets: DataAssetsRequest = None,
                              data_format: Format = None) -> Dict:
        """ Retrieve residual variance data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Residual_Variance, Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_universe_factor_exposure(self,
                                     start_date: dt.date,
                                     end_date: dt.date,
                                     assets: DataAssetsRequest = None,
                                     data_format: Format = None) -> Dict:
        """ Retrieve universe factor exposure data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_factor_returns(self,
                           start_date: dt.date,
                           end_date: dt.date,
                           data_format: Format = None) -> Dict:
        """ Retrieve factor return data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=None,
                                                  measures=[Measure.Factor_Return, Measure.Factor_Name,
                                                            Measure.Factor_Id],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_covariance_matrix(self,
                              start_date: dt.date,
                              end_date: dt.date,
                              data_format: Format = None) -> Dict:
        """ Retrieve covariance matrix data for existing risk model """

        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=None,
                                                  measures=[Measure.Covariance_Matrix, Measure.Factor_Name,
                                                            Measure.Factor_Id],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_issuer_specific_covariance(self,
                                       start_date: dt.date,
                                       end_date: dt.date,
                                       assets: DataAssetsRequest = None,
                                       data_format: Format = None) -> Dict:
        """ Retrieve issuer specific covariance data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Issuer_Specific_Covariance],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_factor_portfolios(self,
                              start_date: dt.date,
                              end_date: dt.date,
                              assets: DataAssetsRequest = None,
                              data_format: Format = None) -> Dict:
        """ Retrieve factor portfolios data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Factor_Portfolios],
                                                  limit_factors=False,
                                                  data_format=data_format)

    def get_data(self,
                 measures: List[Measure],
                 start_date: dt.date,
                 end_date: dt.date,
                 assets: DataAssetsRequest = None,
                 limit_factors: bool = None,
                 data_format: Format = None) -> Dict:
        """ Retrieve data for multiple measures for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=measures,
                                                  limit_factors=limit_factors,
                                                  data_format=data_format)

    def upload_data(self, data: RiskModelData):
        """ Upload risk model data to existing risk model """
        GsRiskModelApi.upload_risk_model_data(self.model.id, data)

    def upload_partial_data(self, data: RiskModelData, target_universe_size: float = None):
        """ Upload partial risk model data to existing risk model, if repeats in partial upload,
            newer posted data will replace existing data on upload day """
        GsRiskModelApi.upload_risk_model_data(self.model.id,
                                              data,
                                              partial_upload=True,
                                              target_universe_size=target_universe_size)
