USE [ParkingManagementSystemCenter]
GO
/****** Object:  StoredProcedure [dbo].[SP_UpdatePHIParkingHistoryDate]    Script Date: 03/06/2025 2:03:37 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[SP_UpdatePHIParkingHistoryDate]
	@StartDate DATETIME2(0),
    @EndDate DATETIME2(0),
	@ParkingId int
AS
BEGIN
		Declare @Object as Int;
		DECLARE @hr  int
		Declare @json_UserView as table(Json_Table_UserView nvarchar(max))
		Declare @json_ClientView as table(Json_Table_ClientView nvarchar(max))
		Declare @url nvarchar(256)
		Declare @string_EndDate nvarchar(256)
		Declare @string_StartDate nvarchar(256)
		Declare @APIToken nvarchar(256)

		set @string_EndDate = convert(varchar(25), @EndDate, 120);
		set @string_StartDate = convert(varchar(25), @StartDate, 120);

		--set @url = 'https://apicarparking.thiso.cloud/api/UserView/GetNumber?number=10';
		set @url = 'https://apicarparking.thiso.cloud/api/UserView/GetTimeOutToTimeIn?EndDate='+@string_EndDate+'&StartDate='+@string_StartDate;
		Exec @hr=sp_OACreate 'MSXML2.ServerXMLHTTP.6.0', @Object OUT;
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'open', NULL, 'get',@url, 'false'
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'send'
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'responseText', @json_UserView OUTPUT
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		INSERT into @json_UserView (Json_Table_UserView) exec sp_OAGetProperty @Object, 'responseText'
		EXEC sp_OADestroy @Object

		set @url = 'https://apicarparking.thiso.cloud/api/ClientView/GetTimeOutToTimeIn?EndDate='+@string_EndDate+'&StartDate='+@string_StartDate;
		Exec @hr=sp_OACreate 'MSXML2.ServerXMLHTTP.6.0', @Object OUT;
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'open', NULL, 'get',@url, 'false'
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'send'
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object
		Exec @hr=sp_OAMethod @Object, 'responseText', @json_ClientView OUTPUT
		IF @hr <> 0 EXEC sp_OAGetErrorInfo @Object	
		INSERT into @json_ClientView (Json_Table_ClientView) exec sp_OAGetProperty @Object, 'responseText'
		EXEC sp_OADestroy @Object

		delete from [ParkingManagementSystemCenter].[dbo].[Table_ParkingHistories] where ExitTime <= @EndDate and ExitTime >= @StartDate and ParkingId = 2

		INSERT INTO [ParkingManagementSystemCenter].[dbo].[Table_ParkingHistories]
		(
		  [ParkingId],
		  [RecordId],
		  [VehicleTypeId],
		  [EntryEmployeeId],
		  [EntryEmployee],
		  [ExitEmployeeId],
		  [ExitEmployee],
		  [CardTypeId],
		  [CardCode],
		  [EntryLicensePlate],
		  [ExitLicensePlate],
		  [EntryTime],
		  [ExitTime],
		  [VoucherTypeId],
		  [VoucherCode],
		  [VoucherValue],
		  [ParkingFee],
		  [Cash],
		  [BankTransfer],
		  [TotalAmount],
		  [ImageIn],
		  [ImageOut],
		  [EntryWorkstation],
		  [ExitWorkstation]
		) 
		select
			@ParkingId	as [ParkingId],
			UserView.[sessionId] as [RecordId],			
			max(ClientView.[vehicleType]) as [VehicleTypeId],			
			'' as [EntryEmployeeId],		
			'' as [EntryEmployee],			
			'' as [ExitEmployeeId],
			'' as [ExitEmployee],	
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then 2 else 1 end as [CardTypeId],
			ClientView.[cardNumber]	as [CardCode],
			max(ClientView.[plateNumberIn]) as [EntryLicensePlate],
			max(ClientView.[plateNumberOut]) as [ExitLicensePlate],
			max(ClientView.[timeIn]) as [EntryTime],
			max(ClientView.[timeOut]) as [ExitTime],
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then 0 else (case when (max(ClientView.[voucherId]) is null) then 0 else 1 end)end as [VoucherTypeId],
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then '' else max(ClientView.[barcode]) end as [VoucherCode],
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then 0 else max(ClientView.[voucherPrice]) end as [VoucherValue],
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then isnull(max(UserView.userPriceType),0) else (cast((isnull(max(ClientView.[price]),0) + isnull(max(ClientView.[voucherPrice]),0))as float)) end as [ParkingFee],
			max(ClientView.[price]) as [Cash],
			0 as [BankTransfer],
			case when ((max(UserView.[userPriceType]) != 0) or (max(UserView.[userPriceType]) is not null)) then 0 else cast((isnull(max(ClientView.[price]),0)) as float) end as [TotalAmount],
			replace('{"front": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageInUrl1]) + '", "extra1": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageInUrl2]) + '", "extra2": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageInUrl1]) + '", "back": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageInUrl2]) + '"}','\','/') as [ImageIn],
			replace('{"front": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageOutUrl1]) + '", "extra1": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageOutUrl2]) + '", "extra2": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageOutUrl1]) + '", "back": "api/Image/ExportImageAll?path=E:\Images\' + max(ClientView.[imageOutUrl2]) + '"}','\','/') as [ImageOut],
			'' as [EntryWorkstation],
			'' as [ExitWorkstation]
		 	FROM 
			(
				(SELECT  
						[timeIn],
						[timeOut],
						[cardId],
						[cardNumber],
						[status],
						[plateNumberIn],
						[plateNumberOut],
						[vehicleType],
						[barcode],
						[price],
						[voucherId],
						[voucherPrice],
						[imageInUrl1],
						[imageInUrl2],
						[imageOutUrl1],
						[imageOutUrl2]
				FROM OPENJSON((select * from @json_ClientView))
				WITH (   
						  [timeIn]					datetime2 N'$.timeIn',
						  [timeOut]					datetime2 N'$.timeOut',
						  [cardId]					nvarchar(256) N'$.cardId',
						  [cardNumber]				nvarchar(256) N'$.cardNumber',
						  [status]					nvarchar(256) N'$.status',
						  [plateNumberIn]			nvarchar(256) N'$.plateNumberIn',
						  [plateNumberOut]			nvarchar(256) N'$.plateNumberOut',
						  [vehicleType]				int N'$.vehicleType',
						  [barcode]					nvarchar(256) N'$.barcode',
						  [price]					float N'$.price',
						  [voucherId]				nvarchar(max) N'$.voucherId',
						  [voucherPrice]			float N'$.voucherPrice',
						  [imageInUrl1]				nvarchar(256) N'$.imageInUrl1',
						  [imageInUrl2]				nvarchar(256) N'$.imageInUrl2',
						  [imageOutUrl1]			nvarchar(256) N'$.imageOutUrl1',
						  [imageOutUrl2]			nvarchar(256) N'$.imageOutUrl2'  
					 )
				)
			) as ClientView left join
			(select*
				FROM
				(
						(SELECT 
							[sessionId],
							[timeIn], 
							[timeOut],
							[price],
							[cardNumber],
							[imageInUrl1],
							[imageInUrl2],
							[imageOutUrl1],
							[imageOutUrl2],
							[userPriceType]
						FROM OPENJSON((select * from @json_UserView))
						WITH 
						(		  [sessionId]				varchar(255) '$.sessionId',
								  [timeIn]					datetime2 N'$.timeIn',
								  [timeOut]					datetime2 N'$.timeOut',
								  [cardId]					nvarchar(256) N'$.cardId',
								  [cardNumber]				nvarchar(256) N'$.cardNumber',
								  [status]					nvarchar(256) N'$.status',
								  [fullName]				nvarchar(256) N'$.fullName',
								  [plateNumber]				nvarchar(256) N'$.plateNumber',
								  [vehicleType]				nvarchar(256) N'$.vehicleType',
								  [group]					nvarchar(256) N'$.group',
								  [price]					nvarchar(256) N'$.price',
								  [voucherPrice]			nvarchar(256) N'$.voucherPrice',
								  [voucherId]				nvarchar(256) N'$.voucherId',
								  [userPriceType]			float N'$.userPriceType',
								  [imageInUrl1]				nvarchar(256) N'$.imageInUrl1',
								  [imageInUrl2]				nvarchar(256) N'$.imageInUrl2',
								  [imageOutUrl1]			nvarchar(256) N'$.imageOutUrl1',
								  [imageOutUrl2]			nvarchar(256) N'$.imageOutUrl2'  
						)
					 )
				) A
			) as UserView on (ClientView.timeOut = UserView.timeOut and ClientView.cardNumber = UserView.cardNumber)
			group by ClientView.timeOut, ClientView.cardNumber 

	INSERT INTO [ParkingManagementSystemCenter].[dbo].[Table_FollowUpdates] (ParkingId,[DateTime])
	values (@ParkingId, @EndDate);

END